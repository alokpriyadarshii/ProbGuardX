-- SQL data manipulation, feature engineering, aggregation, and churn features.
-- Compatible with SQLite for local execution:
--   sqlite3 :memory: ".read data_tools/sql/customer_feature_queries.sql"

DROP TABLE IF EXISTS customer_activity;

CREATE TABLE customer_activity (
    customer_id TEXT PRIMARY KEY,
    region TEXT NOT NULL,
    channel TEXT NOT NULL,
    signup_date TEXT NOT NULL,
    event_date TEXT NOT NULL,
    spend REAL,
    sessions INTEGER,
    support_tickets INTEGER,
    clicked_offer INTEGER,
    churned INTEGER
);

INSERT INTO customer_activity VALUES
('Q001','Urban','online','2025-01-11','2026-01-09',154.30,10,1,1,0),
('Q002','Urban','retail','2025-02-04','2026-01-25',92.10,6,3,0,1),
('Q003','Rural','online','2025-03-13','2026-02-12',118.45,8,2,1,0),
('Q004','Rural','retail','2025-04-22','2026-03-01',61.80,4,4,0,1),
('Q005','Suburban','partner','2025-05-08','2026-03-27',209.50,15,1,1,0),
('Q006','Suburban','online','2025-06-18','2026-04-19',133.75,11,2,1,0),
('Q007','Urban','partner','2025-07-02','2026-05-03',70.25,5,3,0,1),
('Q008','Rural','partner','2025-07-30','2026-05-20',83.60,6,3,0,1),
('Q009','Suburban','retail','2025-08-21','2026-06-01',248.90,17,0,1,0),
('Q010','Urban','online','2025-09-10','2026-06-07',166.40,12,1,1,0),
('Q011','Rural','online','2025-10-17','2026-06-16',55.95,4,4,0,1),
('Q012','Suburban','partner','2025-11-06','2026-06-21',190.20,13,1,1,0);

WITH feature_base AS (
    SELECT
        customer_id,
        region,
        channel,
        julianday(event_date) - julianday(signup_date) AS tenure_days,
        COALESCE(spend, 0.0) AS spend,
        COALESCE(sessions, 0) AS sessions,
        COALESCE(support_tickets, 0) AS support_tickets,
        clicked_offer,
        churned,
        COALESCE(spend, 0.0) / NULLIF(COALESCE(sessions, 0), 0) AS spend_per_session,
        CAST(COALESCE(support_tickets, 0) AS REAL) / NULLIF(COALESCE(sessions, 0), 0) AS support_load
    FROM customer_activity
),
ranked_customers AS (
    SELECT
        *,
        NTILE(4) OVER (ORDER BY spend) AS spend_quartile,
        CASE
            WHEN support_load >= 0.40 THEN 'high'
            WHEN support_load >= 0.10 THEN 'medium'
            ELSE 'low'
        END AS risk_segment
    FROM feature_base
)
SELECT
    region,
    channel,
    COUNT(*) AS customers,
    ROUND(SUM(spend), 2) AS total_spend,
    ROUND(AVG(sessions), 2) AS avg_sessions,
    ROUND(AVG(churned), 3) AS churn_rate,
    ROUND(AVG(clicked_offer), 3) AS offer_click_rate,
    ROUND(AVG(spend_per_session), 2) AS avg_spend_per_session
FROM ranked_customers
GROUP BY region, channel
ORDER BY region, channel;
