# Customer Churn Prediction

End-to-end binary classification project to predict whether a customer may leave a subscription service.

## Dataset disclaimer
`data/customer_churn.csv` is synthetic learning data. It does not contain real customer records and must not be used to make decisions about real customers.

## Features
- tenure_months, monthly_charges
- contract_type, internet_service
- tech_support, paperless_billing, payment_method
- additional_services_count

Target: `churn` (1 = churn, 0 = retained).

## Setup (Python 3.10+)
```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run
```bash
python src/validate_data.py
python src/train.py
streamlit run src/app.py
```

## What you will learn
1. Business problem and target variable.
2. EDA and class distribution.
3. Train/test split with stratification.
4. Numeric and categorical preprocessing.
5. Logistic Regression baseline and Random Forest comparison.
6. Evaluation using precision, recall, F1, ROC-AUC and confusion matrix.
7. A Streamlit prediction interface.

## Important
The sample data uses an artificial churn pattern. Metrics describe only this generated dataset, not real customer behaviour. For real work, use consented, representative data and validate model fairness and business impact.
