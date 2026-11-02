from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data" / "customer_churn.csv"
REQUIRED = {"customer_id","tenure_months","monthly_charges","contract_type",
            "internet_service","tech_support","paperless_billing","payment_method",
            "additional_services_count","churn"}

def main():
    df = pd.read_csv(DATA)
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    if df[list(REQUIRED)].isna().any().any():
        raise ValueError("Missing values found.")
    if not set(df["churn"].unique()).issubset({0,1}):
        raise ValueError("churn must be encoded as 0 or 1.")
    if (df["tenure_months"] < 0).any() or (df["monthly_charges"] < 0).any():
        raise ValueError("Tenure and charges cannot be negative.")
    print(f"VALID: {len(df)} customers | churn rate: {df.churn.mean():.1%}")

if __name__ == "__main__":
    main()
