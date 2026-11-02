-- Churn rate
SELECT ROUND(100.0 * AVG(churn), 2) AS churn_rate_pct
FROM customer_churn;

-- Churn by contract type
SELECT contract_type, COUNT(*) AS customers,
       ROUND(100.0 * AVG(churn), 2) AS churn_rate_pct
FROM customer_churn
GROUP BY contract_type
ORDER BY churn_rate_pct DESC;

-- Churn by tenure band
SELECT CASE
         WHEN tenure_months < 12 THEN '0-11 months'
         WHEN tenure_months < 24 THEN '12-23 months'
         WHEN tenure_months < 48 THEN '24-47 months'
         ELSE '48+ months'
       END AS tenure_band,
       COUNT(*) AS customers,
       ROUND(100.0 * AVG(churn), 2) AS churn_rate_pct
FROM customer_churn
GROUP BY tenure_band
ORDER BY MIN(tenure_months);

-- Churn by payment method
SELECT payment_method, COUNT(*) AS customers,
       ROUND(100.0 * AVG(churn), 2) AS churn_rate_pct
FROM customer_churn
GROUP BY payment_method
ORDER BY churn_rate_pct DESC;
