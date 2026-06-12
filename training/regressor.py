import joblib
import numpy as np
import pandas as pd

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor

from sklearn.metrics import (
    mean_absolute_error,
    r2_score
)

from xgboost import XGBRegressor

import matplotlib.pyplot as plt



# PATHS
PROJECT_DIR = Path(__file__).resolve().parent.parent

DATASET_DIR = PROJECT_DIR / "dataset"

TENSOR_DIR = (
    DATASET_DIR
    / "graphs"
    / "tensors_csv"
)

EMBED_DIR = (
    DATASET_DIR
    / "graphs"
    / "lstm_encoder"
)

OUTPUT_DIR = (
    DATASET_DIR
    / "graphs"
    / "future_value_model"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# LOAD
embeddings = np.load(
    EMBED_DIR
    / "behavior_embeddings.npy"
)

X_static = np.load(
    TENSOR_DIR
    / "X_static_forecast.npy"
)

y = np.load(
    TENSOR_DIR
    / "y_future.npy"
)
y = np.log1p(y)

print(
    "Embeddings:",
    embeddings.shape
)

print(
    "Static:",
    X_static.shape
)

print(
    "Targets:",
    y.shape
)


# MERGE
X = np.concatenate(
    [
        embeddings,
        X_static
    ],
    axis=1
)

print(
    "\nFinal Shape:",
    X.shape
)


# SPLIT
X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42

)

print(
    "\nTrain:",
    X_train.shape
)

print(
    "Test:",
    X_test.shape
)

# MODEL
base_model = XGBRegressor(

    n_estimators=1000,

    max_depth=6,

    learning_rate=0.03,

    subsample=0.8,

    colsample_bytree=0.8,

    objective="reg:squarederror",

    random_state=42,

    n_jobs=-1
)

model = MultiOutputRegressor(
    base_model
)


# TRAIN
model.fit(
    X_train,
    y_train
)


# PREDICT
pred = model.predict(
    X_test
)


# METRICS
target_names = [

    "Future Flights",
    "Future Distance",
    "Future Points"

]

results = []

print("\n" + "=" * 60)

for i, name in enumerate(target_names):

    mae = mean_absolute_error(
        y_test[:, i],
        pred[:, i]
    )

    r2 = r2_score(
        y_test[:, i],
        pred[:, i]
    )

    results.append(
        [name, mae, r2]
    )

    print(
        f"{name}"
    )

    print(
        f"MAE: {mae:.3f}"
    )

    print(
        f"R2 : {r2:.4f}"
    )

    print()

print("=" * 60)


# SAVE METRICS
metrics_df = pd.DataFrame(

    results,

    columns=[
        "Target",
        "MAE",
        "R2"
    ]
)

metrics_df.to_csv(

    OUTPUT_DIR
    / "metrics.csv",

    index=False
)


# FEATURE IMPORTANCE
feature_names = [

    *[
        f"emb_{i}"
        for i in range(32)
    ],

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

    "feature":
    feature_names,

    "importance":
    model.estimators_[0]
    .feature_importances_

})

importance = importance.sort_values(

    "importance",

    ascending=False

)

importance.to_csv(

    OUTPUT_DIR
    / "feature_importance.csv",

    index=False

)

plt.figure(
    figsize=(10, 8)
)

top = importance.head(25)

plt.barh(
    top["feature"],
    top["importance"]
)

plt.gca().invert_yaxis()

plt.tight_layout()

plt.savefig(

    OUTPUT_DIR
    / "feature_importance.png",

    dpi=300

)

plt.close()

# SCATTER PLOT
plt.figure(
    figsize=(8, 8)
)

plt.scatter(

    y_test[:, 0],

    pred[:, 0],

    alpha=0.4

)

plt.xlabel(
    "Actual Flights"
)

plt.ylabel(
    "Predicted Flights"
)

plt.title(
    "Future Flights Prediction"
)

plt.tight_layout()

plt.savefig(

    OUTPUT_DIR
    / "prediction_scatter.png",

    dpi=300

)

plt.close()

# SAVE MODEL
joblib.dump(

    model,

    OUTPUT_DIR
    / "future_value_xgb.pkl"

)

print(
    "\nSaved To:"
)

print(
    OUTPUT_DIR
)