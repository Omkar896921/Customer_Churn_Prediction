from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, roc_auc_score, confusion_matrix)

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data" / "customer_churn.csv"
MODEL_DIR, REPORT_DIR = BASE / "models", BASE / "reports"
TARGET = "churn"
NUMERIC = ["tenure_months","monthly_charges","additional_services_count"]
CATEGORICAL = ["contract_type","internet_service","tech_support",
               "paperless_billing","payment_method"]
FEATURES = NUMERIC + CATEGORICAL

def make_preprocessor():
    num_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])
    cat_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])
    return ColumnTransformer([
        ("numeric", num_pipe, NUMERIC),
        ("categorical", cat_pipe, CATEGORICAL)
    ])

def main():
    df = pd.read_csv(DATA)
    X, y = df[FEATURES], df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    candidates = {
        "Logistic Regression": LogisticRegression(max_iter=2000, class_weight="balanced"),
        "Random Forest": RandomForestClassifier(n_estimators=250, min_samples_leaf=3,
                                                class_weight="balanced", random_state=42)
    }
    results, fitted = {}, {}
    for name, estimator in candidates.items():
        pipe = Pipeline([("preprocess", make_preprocessor()), ("model", estimator)])
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        proba = pipe.predict_proba(X_test)[:,1]
        results[name] = {
            "accuracy": round(accuracy_score(y_test,pred),4),
            "precision": round(precision_score(y_test,pred,zero_division=0),4),
            "recall": round(recall_score(y_test,pred,zero_division=0),4),
            "f1": round(f1_score(y_test,pred,zero_division=0),4),
            "roc_auc": round(roc_auc_score(y_test,proba),4),
            "confusion_matrix": confusion_matrix(y_test,pred).tolist()
        }
        fitted[name] = pipe

    # Choose model by F1 for this teaching example; use cross-validation for rigorous selection.
    best = max(results, key=lambda name: results[name]["f1"])
    MODEL_DIR.mkdir(exist_ok=True); REPORT_DIR.mkdir(exist_ok=True)
    joblib.dump(fitted[best], MODEL_DIR/"customer_churn_model.joblib")
    (REPORT_DIR/"evaluation.json").write_text(
        json.dumps({"selected_model":best,"metrics":results},indent=2), encoding="utf-8")
    pd.DataFrame([{"model":k,**{m:v for m,v in val.items() if m!="confusion_matrix"}}
                  for k,val in results.items()]).to_csv(REPORT_DIR/"model_comparison.csv",index=False)
    print("Model comparison:")
    for name, metrics in results.items():
        print(name, metrics)
    print("Selected model:", best)

if __name__ == "__main__":
    main()
