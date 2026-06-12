import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

 
# PATHS
BASE_DIR = Path(__file__).parent

# OUTPUT FOLDERS
GRAPHS_DIR = BASE_DIR / "graphs"
CSV_DIR = GRAPHS_DIR / "csv"

GRAPHS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

CSV_DIR.mkdir(
    parents=True,
    exist_ok=True
)

print(f"Graphs Folder : {GRAPHS_DIR}")
print(f"CSV Folder    : {CSV_DIR}")

flight_df = pd.read_csv(
    r"C:\shikhar(D drive)\D drive\Personal\iit\dataset\Customer Flight Activity.csv"
)

loyalty_df = pd.read_csv(
    r"C:\shikhar(D drive)\D drive\Personal\iit\dataset\Customer Loyalty History.csv"
)

# AGGREGATE TO CUSTOMER-MONTH
monthly_df = (
    flight_df
    .groupby(
        ["Loyalty Number", "Year", "Month"],
        as_index=False
    )
    .agg({
        "Total Flights": "sum",
        "Distance": "sum",
        "Points Accumulated": "sum",
        "Points Redeemed": "sum",
        "Dollar Cost Points Redeemed": "sum"
    })
)

print("\nMonthly Shape:", monthly_df.shape)

# MAX INACTIVITY STREAK 
def max_zero_streak(series):

    max_streak = 0
    current = 0

    for val in series:

        if val == 0:
            current += 1
            max_streak = max(max_streak, current)

        else:
            current = 0

    return max_streak

# ACTIVITY TREND
def activity_trend(series):

    y = np.array(series)

    x = np.arange(len(y))

    if len(np.unique(y)) <= 1:
        return 0

    return np.polyfit(x, y, 1)[0]

# CUSTOMER FEATURES
customer_features = (
    monthly_df
    .groupby("Loyalty Number")
    .agg({
        "Total Flights": ["sum", "mean", "std", "max"],
        "Distance": ["sum", "mean"],
        "Points Accumulated": ["sum", "mean"],
        "Points Redeemed": ["sum", "mean"]
    })
)

customer_features.columns = [
    "_".join(col)
    for col in customer_features.columns
]

customer_features.reset_index(inplace=True)

# INACTIVITY STREAK
streaks = (
    monthly_df
    .sort_values(
        ["Loyalty Number", "Year", "Month"]
    )
    .groupby("Loyalty Number")["Total Flights"]
    .apply(max_zero_streak)
)

customer_features["max_inactive_streak"] = (
    customer_features["Loyalty Number"]
    .map(streaks)
)

# FLIGHT TREND
trends = (
    monthly_df
    .sort_values(
        ["Loyalty Number", "Year", "Month"]
    )
    .groupby("Loyalty Number")["Total Flights"]
    .apply(activity_trend)
)

customer_features["flight_trend"] = (
    customer_features["Loyalty Number"]
    .map(trends)
)

# FIXED REDEMPTION RATIO
customer_features["redemption_ratio"] = np.where(
    customer_features["Points Accumulated_sum"] > 0,

    customer_features["Points Redeemed_sum"] /
    customer_features["Points Accumulated_sum"],

    0
)

customer_features["redemption_ratio"] = (
    customer_features["redemption_ratio"]
    .clip(0, 5)
)

# MERGE STATIC FEATURES
customer_features = customer_features.merge(
    loyalty_df,
    on="Loyalty Number",
    how="left"
)

# FIX SALARY
customer_features["Salary"] = (
    customer_features["Salary"]
    .clip(lower=0)
)

# SAVE CUSTOMER FEATURES
customer_features_path = CSV_DIR / "customer_features.csv"

customer_features.to_csv(
    customer_features_path,
    index=False
)

print("\nSaved:", customer_features_path)

# LOAD BACK
df = pd.read_csv(customer_features_path)

print("\nShape:", df.shape)

# MISSING VALUES
print("\nMissing Values")

print(
    df.isnull()
    .sum()
    .sort_values(ascending=False)
    .head(20)
)

# HISTOGRAMS
features = [
    "Total Flights_mean",
    "max_inactive_streak",
    "flight_trend",
    "redemption_ratio",
    "CLV"
]

for col in features:

    plt.figure(figsize=(8, 4))

    df[col].hist(
        bins=50
    )

    plt.title(col)

    plt.tight_layout()

    save_path = GRAPHS_DIR / f"{col}_histogram.png"

    plt.savefig(
        save_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Saved: {save_path}")

# SEGMENTATION DATASET
segment_df = df[
    [
        "Total Flights_mean",
        "Total Flights_std",
        "Distance_mean",
        "Points Redeemed_mean",
        "max_inactive_streak",
        "flight_trend",
        "redemption_ratio",
        "CLV"
    ]
].copy()

# LOG TRANSFORM SKEWED FEATURES
for col in [
    "CLV",
    "Distance_mean",
    "Points Redeemed_mean"
]:
    segment_df[col] = np.log1p(
        segment_df[col]
    )

# SAVE SEGMENT DATA
segment_path = CSV_DIR / "segment_dataset.csv"

segment_df.to_csv(
    segment_path,
    index=False
)

print("\nSaved:", segment_path)

# STANDARDIZE
scaler = StandardScaler()

X_scaled = scaler.fit_transform(
    segment_df
)

# ELBOW METHOD
inertia = []

for k in range(2, 11):

    km = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=20
    )

    km.fit(X_scaled)

    inertia.append(
        km.inertia_
    )

    print(
        f"K={k}  Inertia={km.inertia_:.2f}"
    )

# SAVE ELBOW CURVE
plt.figure(figsize=(8, 5))

plt.plot(
    range(2, 11),
    inertia,
    marker="o"
)

plt.xlabel("Number of Clusters (K)")
plt.ylabel("Inertia")
plt.title("KMeans Elbow Curve")

plt.grid(True)

plt.tight_layout()

elbow_path = GRAPHS_DIR / "elbow_curve.png"

plt.savefig(
    elbow_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(f"\nSaved: {elbow_path}")

# SAVE INERTIA TABLE
inertia_df = pd.DataFrame({
    "K": list(range(2, 11)),
    "Inertia": inertia
})

inertia_csv = CSV_DIR / "inertia_values.csv"

inertia_df.to_csv(
    inertia_csv,
    index=False
)

print(f"Saved: {inertia_csv}")

print("\nDONE")

# FINAL CLUSTERING
kmeans = KMeans(
    n_clusters=5,
    random_state=42,
    n_init=20
)

clusters = kmeans.fit_predict(X_scaled)

df["cluster"] = clusters

# Save
df.to_csv(
    CSV_DIR / "customer_segments.csv",
    index=False
)

print("\nCluster Counts")

print(
    df["cluster"]
    .value_counts()
    .sort_index()
)

# CLUSTER PROFILE
profile_cols = [

    "Total Flights_mean",
    "Total Flights_std",
    "Distance_mean",
    "Points Redeemed_mean",
    "max_inactive_streak",
    "flight_trend",
    "redemption_ratio",
    "CLV"

]

cluster_profile = (
    df
    .groupby("cluster")[profile_cols]
    .mean()
)

cluster_counts = (
    df["cluster"]
    .value_counts()
    .sort_index()
    .reset_index()
)

cluster_counts.columns = [
    "cluster",
    "count"
]

cluster_counts.to_csv(
    CSV_DIR / "cluster_counts.csv",
    index=False
)

print("\nCluster Profiles")

print(cluster_profile)

cluster_profile.to_csv(
    CSV_DIR / "cluster_profiles.csv",
    index=True
)

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)

profiles = pd.read_csv("graphs/csv/cluster_profiles.csv")

print(profiles)