import joblib
import numpy as np
import pandas as pd

from pathlib import Path

from rapidfuzz import process

from tensorflow.keras.models import load_model # type: ignore
from xgboost import XGBClassifier
 
# PATHS
PROJECT_DIR = Path(__file__).resolve().parent.parent.parent

DATASET_DIR = PROJECT_DIR / "dataset"

CSV_DIR = DATASET_DIR / "graphs" / "csv"

TENSOR_DIR = DATASET_DIR / "graphs" / "tensors_csv"

LSTM_DIR = DATASET_DIR / "graphs" / "lstm_encoder"

HYBRID_DIR = DATASET_DIR / "graphs" / "hybrid_model"

# LOAD MODELS
print("Loading Models...")

embedding_model = load_model(
    LSTM_DIR / "embedding_model.keras"
)

xgb_model = XGBClassifier()

xgb_model.load_model(
    HYBRID_DIR / "hybrid_xgb.json"
)

print("Models Loaded")

# LOAD PREPROCESSORS
sequence_mean = np.load(
    LSTM_DIR / "sequence_mean.npy"
)

sequence_std = np.load(
    LSTM_DIR / "sequence_std.npy"
)

encoders = joblib.load(
    TENSOR_DIR / "label_encoders.pkl"
)

salary_imputer = joblib.load(
    TENSOR_DIR / "salary_imputer.pkl"
)

static_scaler = joblib.load(
    TENSOR_DIR / "static_scaler.pkl"
)

print("Preprocessors Loaded")

# REQUIRED FEATURES
SEQUENCE_FEATURES = [
    "Total Flights",
    "Distance",
    "Points Accumulated",
    "Points Redeemed",
    "Dollar Cost Points Redeemed"
]

STATIC_FEATURES = [
    "CLV",
    "Salary",
    "Gender",
    "Education",
    "Marital Status",
    "Loyalty Card",
    "Enrollment Type",
    "cluster"
]

REQUIRED_COLUMNS = (
    SEQUENCE_FEATURES +
    STATIC_FEATURES
)
 
# FUZZY COLUMN MATCHING
def fuzzy_column_mapping(df):

    rename_dict = {}

    for col in df.columns:

        result = process.extractOne(
            str(col),
            REQUIRED_COLUMNS
        )

        if result is None:
            continue

        best_match = result[0]
        score = result[1]

        if score >= 80:

            rename_dict[col] = best_match

    df = df.rename(
        columns=rename_dict
    )

    return df

# VALIDATE CSV
def validate_csv(df):

    missing = []

    for col in REQUIRED_COLUMNS:

        if col not in df.columns:

            missing.append(col)

    if len(missing) > 0:

        raise ValueError(
            f"Missing Required Columns: {missing}"
        )
 
# RISK LABEL
def get_risk(probability):

    if probability >= 0.80:
        return "VERY HIGH"

    elif probability >= 0.60:
        return "HIGH"

    elif probability >= 0.40:
        return "MEDIUM"

    else:
        return "LOW"

# LOAD CUSTOMER FROM DATASET
def load_customer_by_id(
    loyalty_number
):

    sequence_df = pd.read_csv(
        CSV_DIR / "sequence_dataset.csv"
    )

    customer_df = pd.read_csv(
        CSV_DIR / "customer_segments.csv"
    )

    sequence_df["date"] = pd.to_datetime(
        sequence_df["date"]
    )

    customer_history = sequence_df[
        sequence_df["Loyalty Number"]
        == loyalty_number
    ].copy()

    if len(customer_history) == 0:

        raise ValueError(
            f"Customer {loyalty_number} not found"
        )

    customer_history = (
        customer_history
        .sort_values("date")
        .tail(12)
    )

    if len(customer_history) != 12:

        raise ValueError(
            "Customer must have exactly "
            "12 months history"
        )

    customer_profile = customer_df[
        customer_df["Loyalty Number"]
        == loyalty_number
    ]

    if len(customer_profile) == 0:

        raise ValueError(
            "Customer profile not found"
        )

    customer_profile = (
        customer_profile
        .iloc[0]
    )

    return (
        customer_history,
        customer_profile
    )

# LOAD CUSTOMER FROM CSV
def load_customer_from_csv(
    csv_file
):

    df = pd.read_csv(
        csv_file
    )

    df = fuzzy_column_mapping(
        df
    )

    validate_csv(
        df
    )

    if len(df) < 12:

        raise ValueError(
            "CSV must contain "
            "at least 12 rows"
        )
    
    if "date" in df.columns:
        
        df["date"] = pd.to_datetime(
            df["date"]
        )
        
        df = df.sort_values(
            "date"
        )

    history = (
        df
        .tail(12)
        .copy()
    )

    profile = (
        history
        .iloc[-1]
    )

    return (
        history,
        profile
    )
    

# PREPARE SEQUENCE
def prepare_sequence(
    history
):

    seq = history[
        SEQUENCE_FEATURES
    ].values.astype(
        np.float32
    )

    seq = (
        seq - sequence_mean
    ) / (
        sequence_std + 1e-8
    )

    seq = np.expand_dims(
        seq,
        axis=0
    )

    return seq

# SAFE ENCODING
def safe_encode(
    encoder,
    value
):

    value = str(value)

    classes = set(
        encoder.classes_
    )

    if value not in classes:

        value = encoder.classes_[0]

    return encoder.transform(
        [value]
    )[0]

# PREPARE STATIC
def prepare_static(
    profile
):

    salary = salary_imputer.transform(
        [[profile["Salary"]]]
    )[0][0]

    gender = safe_encode(
        encoders["Gender"],
        profile["Gender"]
    )

    education = safe_encode(
        encoders["Education"],
        profile["Education"]
    )

    marital = safe_encode(
        encoders["Marital Status"],
        profile["Marital Status"]
    )

    loyalty = safe_encode(
        encoders["Loyalty Card"],
        profile["Loyalty Card"]
    )

    enrollment = safe_encode(
        encoders["Enrollment Type"],
        profile["Enrollment Type"]
    )

    numeric = np.array([
        [
            float(profile["CLV"]),
            float(salary)
        ]
    ])

    numeric = static_scaler.transform(
        numeric
    )[0]

    static_vector = np.array([
        [
            numeric[0],
            numeric[1],

            gender,
            education,
            marital,

            loyalty,
            enrollment,

            float(profile["cluster"])
        ]
    ],
    dtype=np.float32)

    return static_vector

def load_customer_from_dataframe(
    df
):

    df = fuzzy_column_mapping(
        df.copy()
    )

    validate_csv(
        df
    )

    if "date" in df.columns:

        df["date"] = pd.to_datetime(
            df["date"]
        )

        df = df.sort_values(
            "date"
        )

    history = (
        df.tail(12)
        .copy()
    )

    profile = (
        history.iloc[-1]
    )

    return (
        history,
        profile
    )

# MAIN PREDICTION
def predict_customer(
    loyalty_number=None,
    csv_file=None,
    dataframe=None
):

    if loyalty_number is not None:

        history, profile = (
            load_customer_by_id(
                loyalty_number
            )
        )

        customer_id = loyalty_number

    elif dataframe is not None:

        history, profile = (
            load_customer_from_dataframe(
                dataframe
            )
        )

        customer_id = "DATAFRAME"

    elif csv_file is not None:

        history, profile = (
            load_customer_from_csv(
                csv_file
            )
        )

        customer_id = "CSV_UPLOAD"

    else:

        raise ValueError(
            "Provide loyalty_number, csv_file or dataframe"
        )

    sequence = prepare_sequence(
        history
    )

    embedding = (
        embedding_model
        .predict(
            sequence,
            verbose=0
        )
    )

    static_vector = (
        prepare_static(
            profile
        )
    )

    X = np.concatenate(
        [
            embedding,
            static_vector
        ],
        axis=1
    )

    probability = float(
        xgb_model
        .predict_proba(X)[0, 1]
    )

    prediction = int(
        probability >= 0.50
    )

    risk = get_risk(
        probability
    )

    result = {

        "customer_id":
        customer_id,

        "churn_probability":
        round(
            probability,
            4
        ),

        "prediction":
        prediction,

        "risk_level":
        risk,

        "segment":
        int(
            profile["cluster"]
        ),

        "clv":
        float(
            profile["CLV"]
        ),

        "salary":
        float(
            profile["Salary"]
        ),

        "loyalty_card":
        str(
            profile["Loyalty Card"]
        ),

        "embedding":
        embedding,

        "static_vector":
        static_vector,

        "model":
        "Hybrid LSTM + XGBoost"

    }

    return result

# TEST
if __name__ == "__main__":

    result = predict_customer(
        loyalty_number=100018
    )

    print("\nPrediction Result\n")

    for k, v in result.items():

        print(
            f"{k}: {v}"
        )
    result = predict_customer(
        loyalty_number=100018
    )
    
    print(result.keys())