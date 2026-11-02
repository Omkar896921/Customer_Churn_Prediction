CREATE TABLE customer_churn (
    customer_id VARCHAR(20) PRIMARY KEY,
    tenure_months INTEGER NOT NULL CHECK (tenure_months >= 0),
    monthly_charges NUMERIC(10,2) NOT NULL CHECK (monthly_charges >= 0),
    contract_type VARCHAR(30) NOT NULL,
    internet_service VARCHAR(30) NOT NULL,
    tech_support VARCHAR(5) NOT NULL,
    paperless_billing VARCHAR(5) NOT NULL,
    payment_method VARCHAR(30) NOT NULL,
    additional_services_count INTEGER NOT NULL CHECK (additional_services_count >= 0),
    churn SMALLINT NOT NULL CHECK (churn IN (0,1))
);
