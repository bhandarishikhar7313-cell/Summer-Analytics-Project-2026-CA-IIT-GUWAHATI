import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer

# PATHS
BASE_DIR = Path(__file__).parent.parent

CSV_DIR = BASE_DIR / "graphs" / "csv"
TENSOR_DIR = BASE_DIR / "graphs" / "tensors_csv"

TENSOR_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# LOAD FILES
sequence_df = pd.read_csv(
    CSV_DIR / "sequence_dataset.csv"
)

customer_df = pd.read_csv(
    CSV_DIR / "customer_segments.csv"
)

print("Sequence Shape:", sequence_df.shape)
print("Customer Shape:", customer_df.shape)

# DATE
sequence_df["date"] = pd.to_datetime(
    sequence_df["date"]
)

sequence_df = sequence_df.sort_values(
    ["Loyalty Number", "date"]
)

# SEQUENCE FEATURES
sequence_features = [
    "Total Flights",
    "Distance",
    "Points Accumulated",
    "Points Redeemed",
    "Dollar Cost Points Redeemed"
]

# BUILD FORECAST DATASET
X_seq = []
y = []

valid_customer_ids = []

skip_count = 0

customer_ids = sorted(
    sequence_df["Loyalty Number"].unique()
)

for customer_id in customer_ids:

    customer_data = sequence_df[
        sequence_df["Loyalty Number"] == customer_id
    ]

    # INPUT WINDOW
    past_window = customer_data[
        customer_data["date"] < "2018-01-01"
    ]

    if len(past_window) != 12:
        skip_count += 1
        continue

    seq = past_window[
        sequence_features
    ].values.astype(np.float32)

    # FUTURE WINDOW
    future_window = customer_data[
        (customer_data["date"] >= "2018-01-01")
        &
        (customer_data["date"] <= "2018-06-30")
    ]

    # INACTIVITY STREAK
    flights = future_window[
        "Total Flights"
    ].values

    max_streak = 0
    current = 0

    for f in flights:

        if f == 0:

            current += 1

            if current > max_streak:
                max_streak = current

        else:

            current = 0

    # CANCELLATION CHECK
    row = customer_df[
        customer_df["Loyalty Number"]
        == customer_id
    ]

    cancel_year = row[
        "Cancellation Year"
    ].values[0]

    cancel_month = row[
        "Cancellation Month"
    ].values[0]

    churn = 0

    if pd.notna(cancel_year):

        if (
            cancel_year == 2018
            and pd.notna(cancel_month)
            and cancel_month <= 6
        ):
            churn = 1

    if max_streak >= 6:
        churn = 1

    X_seq.append(seq)
    y.append(churn)

    valid_customer_ids.append(
        customer_id
    )

print(f"\nSkipped Customers: {skip_count}")

# CONVERT
X_seq = np.array(
    X_seq,
    dtype=np.float32
)

y = np.array(
    y,
    dtype=np.int64
)

print("\nX_seq Shape:", X_seq.shape)
print("y Shape:", y.shape)

print("\nChurn Distribution")

unique, counts = np.unique(
    y,
    return_counts=True
)

for u, c in zip(unique, counts):
    print(f"Class {u}: {c}")

# STATIC FEATURES
customer_df = (
    customer_df
    .set_index("Loyalty Number")
    .loc[valid_customer_ids]
    .reset_index()
)

static_features = [
    "CLV",
    "Salary",
    "Gender",
    "Education",
    "Marital Status",
    "Loyalty Card",
    "Enrollment Type",
    "cluster"
]

X_static_df = customer_df[
    static_features
].copy()

# IMPUTE SALARY
salary_imputer = SimpleImputer(
    strategy="median"
)

X_static_df["Salary"] = (
    salary_imputer
    .fit_transform(
        X_static_df[["Salary"]]
    )
    .ravel()
)

# ENCODE CATEGORICALS
categorical_cols = [
    "Gender",
    "Education",
    "Marital Status",
    "Loyalty Card",
    "Enrollment Type"
]

encoders = {}

for col in categorical_cols:

    le = LabelEncoder()

    X_static_df[col] = le.fit_transform(
        X_static_df[col].astype(str)
    )

    encoders[col] = le
    

# SCALE NUMERICS
numeric_cols = [
    "CLV",
    "Salary"
]

scaler = StandardScaler()

X_static_df[numeric_cols] = (
    scaler.fit_transform(
        X_static_df[numeric_cols]
    )
)

X_static = X_static_df.values.astype(
    np.float32
)

print("\nX_static Shape:", X_static.shape)

# SANITY CHECK
assert X_seq.shape[0] == X_static.shape[0]
assert X_seq.shape[0] == y.shape[0]

print("\nSanity Check Passed")

# SAVE
np.save(
    TENSOR_DIR / "X_seq_forecast.npy",
    X_seq
)

np.save(
    TENSOR_DIR / "X_static_forecast.npy",
    X_static
)

np.save(
    TENSOR_DIR / "y_forecast.npy",
    y
)

print("\nSaved Files")

print("X_seq_forecast.npy")
print("X_static_forecast.npy")
print("y_forecast.npy")

print("\nFinal Shapes")

print("X_seq    :", X_seq.shape)
print("X_static :", X_static.shape)
print("y        :", y.shape)


# SAVE PREPROCESSORS
joblib.dump(
    encoders,
    TENSOR_DIR / "label_encoders.pkl"
)

joblib.dump(
    salary_imputer,
    TENSOR_DIR / "salary_imputer.pkl"
)

joblib.dump(
    scaler,
    TENSOR_DIR / "static_scaler.pkl"
)

print("\nSaved Preprocessors")

print("label_encoders.pkl")
print("salary_imputer.pkl")
print("static_scaler.pkl")