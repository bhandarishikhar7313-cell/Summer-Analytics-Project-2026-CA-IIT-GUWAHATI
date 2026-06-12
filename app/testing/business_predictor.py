import joblib
import numpy as np

from pathlib import Path

from testing.inference import predict_customer

from testing.retention_engine import (
    generate_retention_profile
)

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent

FUTURE_DIR = (
    PROJECT_DIR
    / "dataset"
    / "graphs"
    / "future_value_model"
)

print("Loading Future Value Model...")

future_model = joblib.load(
    FUTURE_DIR
    / "future_value_xgb.pkl"
)

print("Future Value Model Loaded")

def predict_business_profile(

    loyalty_number=None,
    csv_file=None,
    dataframe=None

):

    prediction = predict_customer(

        loyalty_number=loyalty_number,

        csv_file=csv_file,

        dataframe=dataframe

    )

    print("\nCustomer Loaded")

    print(
        f"Churn Probability: "
        f"{prediction['churn_probability']}"
    )
    
    embedding = prediction[
        "embedding"
    ]

    static_vector = prediction[
        "static_vector"
    ]

    X_future = np.concatenate(

        [
            embedding,
            static_vector
        ],

        axis=1

    )

    print(
        "\nFuture Model Input Shape:",
        X_future.shape
    )
    
    future_pred = future_model.predict(
        X_future
    )

    future_pred = np.expm1(
        future_pred
    )
    
    future_flights = float(
        future_pred[0][0]
    )

    future_distance = float(
        future_pred[0][1]
    )

    future_points = float(
        future_pred[0][2]
    )

    print("\nFuture Predictions")

    print(
        "Flights:",
        round(
            future_flights,
            2
        )
    )

    print(
        "Distance:",
        round(
            future_distance,
            2
        )
    )

    print(
        "Points:",
        round(
            future_points,
            2
        )
    )
    
    profile = generate_retention_profile(

        cluster=
        prediction["segment"],

        churn_probability=
        prediction["churn_probability"],

        future_flights=
        future_flights,

        future_distance=
        future_distance,

        future_points=
        future_points,

        clv=
        prediction["clv"],

        salary=
        prediction["salary"],

        loyalty_card=
        prediction["loyalty_card"]

    )

    return profile

if __name__ == "__main__":

    profile = predict_business_profile(

        loyalty_number=100018

    )

    print("\nFINAL PROFILE")

    for k, v in profile.items():

        print(
            f"{k}: {v}"
        )