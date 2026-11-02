# Metrics guide

- **Accuracy**: fraction of all predictions that are correct.
- **Precision**: among customers predicted to churn, fraction who actually churn.
- **Recall**: among customers who churn, fraction correctly identified.
- **F1-score**: harmonic mean of precision and recall.
- **ROC-AUC**: how well the model ranks churners above non-churners across thresholds.

Business trade-off:
- False positive: a retained customer is incorrectly flagged as likely to churn; unnecessary retention offer may be sent.
- False negative: a customer who churns is missed; a retention opportunity may be lost.

Choose thresholds based on campaign cost, customer experience and expected retention value, not accuracy alone.
