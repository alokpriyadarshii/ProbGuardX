# R data manipulation, aggregation, and model-ready feature engineering example.
# Run from the project root:
#   Rscript data_tools/r/customer_feature_engineering.R

args <- commandArgs(trailingOnly = TRUE)
data_path <- if (length(args) >= 1) args[[1]] else "data_tools/r/r_customer_activity.csv"

customer_activity <- read.csv(data_path, stringsAsFactors = FALSE)
customer_activity$signup_date <- as.Date(customer_activity$signup_date)
customer_activity$event_date <- as.Date(customer_activity$event_date)
customer_activity$spend[is.na(customer_activity$spend)] <- median(customer_activity$spend, na.rm = TRUE)
customer_activity$sessions[is.na(customer_activity$sessions)] <- 0
customer_activity$support_tickets[is.na(customer_activity$support_tickets)] <- 0

customer_activity$tenure_days <- as.integer(customer_activity$event_date - customer_activity$signup_date)
customer_activity$spend_per_session <- customer_activity$spend / pmax(customer_activity$sessions, 1)
customer_activity$support_load <- customer_activity$support_tickets / pmax(customer_activity$sessions, 1)
customer_activity$risk_segment <- cut(
  customer_activity$support_load,
  breaks = c(-Inf, 0.10, 0.40, Inf),
  labels = c("low", "medium", "high")
)

summary_table <- aggregate(
  cbind(spend, sessions, churned, clicked_offer) ~ region + channel,
  data = customer_activity,
  FUN = mean
)
names(summary_table) <- c(
  "region", "channel", "avg_spend", "avg_sessions", "churn_rate", "offer_click_rate"
)

print("Aggregated customer features by region/channel")
print(summary_table)

churn_model <- glm(
  churned ~ support_tickets + clicked_offer + spend_per_session + tenure_days,
  data = customer_activity,
  family = binomial(),
  control = glm.control(maxit = 100)
)

customer_activity$predicted_churn_probability <- predict(churn_model, type = "response")
print("Top churn-risk customers")
print(customer_activity[order(-customer_activity$predicted_churn_probability),
                        c("customer_id", "region", "channel", "churned", "predicted_churn_probability")][1:8, ])
