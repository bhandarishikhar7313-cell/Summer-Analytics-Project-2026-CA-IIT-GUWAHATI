import numpy as np
import pandas as pd

from pathlib import Path

from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
    RocCurveDisplay
)

from xgboost import XGBClassifier

import matplotlib.pyplot as plt

# PATHS
PROJECT_DIR = Path(__file__).resolve().parent.parent

DATASET_DIR = PROJECT_DIR / "dataset"

TENSOR_DIR = (
    DATASET_DIR
    / "graphs"
    / "tensors_csv"
)

OUTPUT_DIR = (
    DATASET_DIR
    / "graphs"
    / "forecast_baseline"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# LOAD TENSORS
X_static = np.load(
    TENSOR_DIR / "X_static_forecast.npy"
)

y = np.load(
    TENSOR_DIR / "y_forecast.npy"
)

print("X_static Shape:", X_static.shape)
print("y Shape:", y.shape)

# TRAIN TEST SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X_static,
    y,
    test_size=0.20,
    stratify=y,
    random_state=42
)

print("\nTrain:", X_train.shape)
print("Test :", X_test.shape)

# CLASS WEIGHT
neg = np.sum(y_train == 0)
pos = np.sum(y_train == 1)

scale_pos_weight = neg / max(pos, 1)

print(
    "\nscale_pos_weight:",
    round(scale_pos_weight, 3)
)

# MODEL
model = XGBClassifier(
    n_estimators=500,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=scale_pos_weight,
    eval_metric="logloss",
    random_state=42,
    n_jobs=-1
)

model.fit(
    X_train,
    y_train
)

# PREDICTIONS
y_pred = model.predict(
    X_test
)

y_prob = model.predict_proba(
    X_test
)[:, 1]

# METRICS
acc = accuracy_score(
    y_test,
    y_pred
)

prec = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

rec = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

if len(np.unique(y_test)) > 1:
    auc = roc_auc_score(
        y_test,
        y_prob
    )
else:
    auc = 0.0

print("\n" + "=" * 60)

print("Accuracy :", round(acc, 4))
print("Precision:", round(prec, 4))
print("Recall   :", round(rec, 4))
print("F1 Score :", round(f1, 4))
print("ROC AUC  :", round(auc, 4))

print("=" * 60)

# CONFUSION MATRIX
cm = confusion_matrix(
    y_test,
    y_pred
)

print("\nConfusion Matrix")

print(cm)

print("\nClassification Report")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)

# ROC CURVE
if len(np.unique(y_test)) > 1:

    plt.figure(figsize=(8, 6))

    RocCurveDisplay.from_predictions(
        y_test,
        y_prob
    )

    plt.title(
        "Forecast Baseline ROC Curve"
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "roc_curve.png",
        dpi=300
    )

    plt.close()

# FEATURE IMPORTANCE
feature_names = [
    "CLV",
    "Salary",
    "Gender",
    "Education",
    "Marital Status",
    "Loyalty Card",
    "Enrollment Type",
    "Cluster"
]

importance = pd.DataFrame({
    "feature": feature_names,
    "importance": model.feature_importances_
})

importance = importance.sort_values(
    "importance",
    ascending=False
)

print("\nFeature Importance")

print(importance)

importance.to_csv(
    OUTPUT_DIR / "feature_importance.csv",
    index=False
)

plt.figure(figsize=(10, 6))

plt.barh(
    importance["feature"],
    importance["importance"]
)

plt.gca().invert_yaxis()

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "feature_importance.png",
    dpi=300
)

plt.close()

# SAVE MODEL
model.save_model(
    str(
        OUTPUT_DIR
        / "forecast_xgb_baseline.json"
    )
)

print("\nSaved To:")
print(OUTPUT_DIR)