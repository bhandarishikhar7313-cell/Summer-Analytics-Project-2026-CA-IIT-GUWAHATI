import pandas as pd
import numpy as np

from pathlib import Path

# PATHS
PROJECT_DIR = Path(__file__).resolve().parent.parent

DATASET_DIR = PROJECT_DIR / "dataset"

CSV_DIR = (
    DATASET_DIR
    / "graphs"
    / "csv"
)

# LOAD
customer_df = pd.read_csv(
    CSV_DIR / "customer_segments.csv"
)

print("\nDataset Shape:")
print(customer_df.shape)

print("\nColumns:")
print(customer_df.columns.tolist())

# CLUSTER COUNTS
print("\n" + "=" * 60)
print("CLUSTER DISTRIBUTION")
print("=" * 60)

print(
    customer_df["cluster"]
    .value_counts()
    .sort_index()
)

# NUMERIC SUMMARY
numeric_cols = []

candidate_cols = [

    "CLV",
    "Salary",

    "Total Flights",
    "Distance",

    "Points Accumulated",
    "Points Redeemed"

]

for col in candidate_cols:

    if col in customer_df.columns:
        numeric_cols.append(col)

print("\n" + "=" * 60)
print("NUMERIC CLUSTER PROFILE")
print("=" * 60)

if len(numeric_cols) > 0:

    cluster_numeric = (

        customer_df
        .groupby("cluster")[numeric_cols]
        .mean()
        .round(2)

    )

    print(cluster_numeric)

else:

    print(
        "No numeric columns found."
    )

# CATEGORICAL SUMMARY
categorical_cols = [

    "Loyalty Card",
    "Enrollment Type",
    "Gender",
    "Education",
    "Marital Status"

]

print("\n" + "=" * 60)
print("TOP CATEGORIES PER CLUSTER")
print("=" * 60)

for col in categorical_cols:

    if col not in customer_df.columns:
        continue

    print(f"\n{col}")

    for cluster_id in sorted(
        customer_df["cluster"].unique()
    ):

        mode_value = (

            customer_df[
                customer_df["cluster"]
                == cluster_id
            ][col]

            .mode()

        )

        if len(mode_value) > 0:

            print(
                f"Cluster {cluster_id}: "
                f"{mode_value.iloc[0]}"
            )

# DETAILED CLUSTER REPORT
print("\n" + "=" * 60)
print("DETAILED CLUSTER REPORT")
print("=" * 60)

for cluster_id in sorted(
    customer_df["cluster"].unique()
):

    subset = customer_df[
        customer_df["cluster"]
        == cluster_id
    ]

    print("\n" + "-" * 60)

    print(
        f"Cluster {cluster_id}"
    )

    print(
        f"Customers: {len(subset)}"
    )

    if "CLV" in subset.columns:

        print(
            "Avg CLV:",
            round(
                subset["CLV"].mean(),
                2
            )
        )

    if "Salary" in subset.columns:

        print(
            "Avg Salary:",
            round(
                subset["Salary"].mean(),
                2
            )
        )

    if "Loyalty Card" in subset.columns:

        loyalty_mode = (
            subset["Loyalty Card"]
            .mode()
        )

        if len(loyalty_mode):

            print(
                "Top Loyalty Card:",
                loyalty_mode.iloc[0]
            )

    if "Enrollment Type" in subset.columns:

        enroll_mode = (
            subset["Enrollment Type"]
            .mode()
        )

        if len(enroll_mode):

            print(
                "Top Enrollment Type:",
                enroll_mode.iloc[0]
            )

# SAVE SUMMARY
OUTPUT_DIR = (
    DATASET_DIR
    / "graphs"
    / "cluster_analysis"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

summary_rows = []

for cluster_id in sorted(
    customer_df["cluster"].unique()
):

    subset = customer_df[
        customer_df["cluster"]
        == cluster_id
    ]

    row = {

        "cluster":
        cluster_id,

        "customers":
        len(subset)

    }

    if "CLV" in subset.columns:

        row["avg_clv"] = round(
            subset["CLV"].mean(),
            2
        )

    if "Salary" in subset.columns:

        row["avg_salary"] = round(
            subset["Salary"].mean(),
            2
        )

    summary_rows.append(row)

summary_df = pd.DataFrame(
    summary_rows
)

summary_df.to_csv(

    OUTPUT_DIR
    / "cluster_summary.csv",

    index=False

)

print("\nSaved:")
print(
    OUTPUT_DIR
    / "cluster_summary.csv"
)

cluster_summary = customer_df.groupby(
    "cluster"
).agg({

    "CLV": "mean",

    "Total Flights_sum": "mean",

    "Distance_sum": "mean",

    "Points Accumulated_sum": "mean",

    "Points Redeemed_sum": "mean",

    "max_inactive_streak": "mean",

    "flight_trend": "mean",

    "redemption_ratio": "mean"

}).round(2)

print(cluster_summary)