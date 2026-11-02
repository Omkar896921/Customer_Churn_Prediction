from pathlib import Path
import joblib
import pandas as pd
import streamlit as st

BASE = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE/"models"/"customer_churn_model.joblib"
st.set_page_config(page_title="Customer Churn Predictor", layout="centered")
st.title("Customer Churn Prediction")
st.caption("Educational demo using synthetic data only.")

if not MODEL_PATH.exists():
    st.error("Model not found. Run: python src/train.py")
    st.stop()

model = joblib.load(MODEL_PATH)
with st.form("customer_form"):
    tenure = st.number_input("Tenure (months)", min_value=0, max_value=120, value=12)
    charges = st.number_input("Monthly charges", min_value=0.0, value=70.0, step=5.0)
    contract = st.selectbox("Contract type", ["Month-to-month","One year","Two year"])
    internet = st.selectbox("Internet service", ["Fiber optic","DSL","No"])
    support = st.selectbox("Tech support", ["Yes","No"])
    paperless = st.selectbox("Paperless billing", ["Yes","No"])
    payment = st.selectbox("Payment method", ["Electronic check","Mailed check","Bank transfer","Credit card"])
    services = st.number_input("Additional services count", min_value=0, max_value=10, value=3)
    submitted = st.form_submit_button("Predict churn risk")

if submitted:
    row = pd.DataFrame([{
        "tenure_months":tenure, "monthly_charges":charges,
        "contract_type":contract, "internet_service":internet,
        "tech_support":support, "paperless_billing":paperless,
        "payment_method":payment, "additional_services_count":services
    }])
    probability = float(model.predict_proba(row)[0,1])
    st.metric("Model-estimated churn probability", f"{probability:.1%}")
    if probability >= 0.5:
        st.warning("Model places this sample in the higher churn-risk group.")
    else:
        st.success("Model places this sample in the lower churn-risk group.")
    st.info("This synthetic demo is not a reliable assessment of any real customer.")
