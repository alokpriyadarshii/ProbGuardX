/* SAS data manipulation, PROC SQL, summary statistics, and logistic modeling.
   Run from the project root in SAS Studio or Base SAS.
*/

%let project_root = .;
%let csv_path = &project_root./data_tools/sas/sas_customer_activity.csv;

proc import datafile="&csv_path"
    out=work.customer_activity
    dbms=csv
    replace;
    guessingrows=max;
run;

data work.customer_features;
    set work.customer_activity;
    signup_dt = input(signup_date, yymmdd10.);
    event_dt = input(event_date, yymmdd10.);
    format signup_dt event_dt yymmdd10.;
    tenure_days = event_dt - signup_dt;
    if sessions <= 0 then spend_per_session = .;
    else spend_per_session = spend / sessions;
    if sessions <= 0 then support_load = .;
    else support_load = support_tickets / sessions;
    if support_load >= 0.40 then risk_segment = "high";
    else if support_load >= 0.10 then risk_segment = "medium";
    else risk_segment = "low";
run;

proc sql;
    create table work.region_channel_summary as
    select
        region,
        channel,
        count(distinct customer_id) as customers,
        sum(spend) as total_spend format=dollar12.2,
        mean(sessions) as avg_sessions format=8.2,
        mean(churned) as churn_rate format=percent8.2,
        mean(clicked_offer) as offer_click_rate format=percent8.2
    from work.customer_features
    group by region, channel
    order by region, channel;
quit;

proc means data=work.customer_features n mean median std min max;
    class region channel;
    var spend sessions support_tickets tenure_days spend_per_session;
run;

proc freq data=work.customer_features;
    tables region*churned channel*clicked_offer risk_segment*churned / chisq;
run;

proc logistic data=work.customer_features descending;
    model churned = support_tickets clicked_offer spend_per_session tenure_days;
    output out=work.churn_scores pred=predicted_churn_probability;
run;
