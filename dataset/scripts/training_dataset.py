import pandas as pd
import numpy as np
from pathlib import Path
 
# PATHS
BASE_DIR = Path(__file__).parent

flight_df = pd.read_csv(
    r"C:\shikhar(D drive)\D drive\Personal\iit\dataset\Customer Flight Activity.csv"
)

loyalty_df = pd.read_csv(
    r"C:\shikhar(D drive)\D drive\Personal\iit\dataset\Customer Loyalty History.csv"
)

segments_df = pd.read_csv(
    BASE_DIR / "graphs" / "csv" / "customer_segments.csv"
)

# MONTHLY AGGREGATION
monthly_df = (
    flight_df
    .groupby(
        ["Loyalty Number", "Year", "Month"],
        as_index=False
    )
    .agg({
        "Total Flights":"sum",
        "Distance":"sum",
        "Points Accumulated":"sum",
        "Points Redeemed":"sum",
        "Dollar Cost Points Redeemed":"sum"
    })
)

# CREATE DATE
monthly_df["date"] = pd.to_datetime(
    monthly_df["Year"].astype(str)
    + "-"
    + monthly_df["Month"].astype(str)
    + "-01"
)

# COMPLETE CUSTOMER TIMELINE
all_months = pd.date_range(
    "2017-01-01",
    "2018-12-01",
    freq="MS"
)

sequence_rows = []

feature_cols = [
    "Total Flights",
    "Distance",
    "Points Accumulated",
    "Points Redeemed",
    "Dollar Cost Points Redeemed"
]

for customer_id in monthly_df["Loyalty Number"].unique():

    customer_data = monthly_df[
        monthly_df["Loyalty Number"] == customer_id
    ]

    customer_data = (
        customer_data
        .set_index("date")
        .reindex(all_months)
    )

    customer_data["Loyalty Number"] = customer_id

    customer_data[feature_cols] = (
        customer_data[feature_cols]
        .fillna(0)
    )

    customer_data = customer_data.reset_index()

    customer_data.rename(
        columns={"index":"date"},
        inplace=True
    )

    sequence_rows.append(
        customer_data
    )

sequence_df = pd.concat(
    sequence_rows,
    ignore_index=True
)

print(
    "Sequence Shape:",
    sequence_df.shape
)

# CHURN LABEL
def max_zero_streak(series):

    max_streak = 0
    current = 0

    for x in series:

        if x == 0:
            current += 1
            max_streak = max(
                max_streak,
                current
            )

        else:
            current = 0

    return max_streak

streaks = (
    sequence_df
    .groupby("Loyalty Number")
    ["Total Flights"]
    .apply(max_zero_streak)
)

labels = pd.DataFrame({
    "Loyalty Number": streaks.index,
    "max_inactive_streak": streaks.values
})

labels = labels.merge(
    loyalty_df[
        [
            "Loyalty Number",
            "Cancellation Year"
        ]
    ],
    on="Loyalty Number",
    how="left"
)

labels["churn"] = np.where(

    (
        labels["Cancellation Year"]
        .notna()
    )
    |
    (
        labels["max_inactive_streak"] >= 6
    ),

    1,

    0
)

print("\nChurn Distribution")

print(
    labels["churn"]
    .value_counts()
)

# MERGE SEGMENTS
labels = labels.merge(
    segments_df[
        [
            "Loyalty Number",
            "cluster"
        ]
    ],
    on="Loyalty Number",
    how="left"
)

# SAVE LABELS
labels.to_csv(
    BASE_DIR
    / "graphs"
    / "csv"
    / "training_labels.csv",
    index=False
)

# SAVE SEQUENCES
sequence_df.to_csv(
    BASE_DIR
    / "graphs"
    / "csv"
    / "sequence_dataset.csv",
    index=False
)

print(
    "\nSaved training_labels.csv"
)

print(
    "Saved sequence_dataset.csv"
)