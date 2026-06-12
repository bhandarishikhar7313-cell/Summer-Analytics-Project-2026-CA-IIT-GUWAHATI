import pandas as pd
import numpy as np

# LOAD DATASETS
flight_df = pd.read_csv("C:\shikhar(D drive)\D drive\Personal\iit\dataset\Customer Flight Activity.csv")
loyalty_df = pd.read_csv("C:\shikhar(D drive)\D drive\Personal\iit\dataset\Customer Loyalty History.csv")
calendar_df = pd.read_csv("C:\shikhar(D drive)\D drive\Personal\iit\dataset\Calendar.csv")
dict_df = pd.read_csv("C:\shikhar(D drive)\D drive\Personal\iit\dataset\Airline Loyalty Data Dictionary.csv")

# BASIC DATASET INFO
datasets = {
    "Flight Activity": flight_df,
    "Loyalty History": loyalty_df,
    "Calendar": calendar_df,
    "Data Dictionary": dict_df
}

for name, df in datasets.items():

    print("\n" + "="*80)
    print(f"{name.upper()}")
    print("="*80)

    # Shape
    print(f"\nShape: {df.shape}")

    # Column names
    print("\nColumns:")
    print(df.columns.tolist())

    # Data types
    print("\nData Types:")
    print(df.dtypes)

    # Missing values
    print("\nMissing Values:")
    missing = df.isnull().sum()
    missing = missing[missing > 0]

    if len(missing) == 0:
        print("No missing values")
    else:
        print(missing.sort_values(ascending=False))

    # Duplicate rows
    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    # First few rows
    print("\nSample Rows:")
    print(df.head())

# FLIGHT ACTIVITY SPECIFIC CHECKS
print("\n" + "="*80)
print("FLIGHT ACTIVITY DEEP CHECKS")
print("="*80)

# Unique customers
print("\nUnique Customers:")
print(flight_df["Loyalty Number"].nunique())

# Date coverage
print("\nYear Range:")
print(flight_df["Year"].min(), "to", flight_df["Year"].max())

# Monthly coverage
print("\nMonth Distribution:")
print(flight_df["Month"].value_counts().sort_index())

# Customer sequence lengths
sequence_lengths = (
    flight_df.groupby("Loyalty Number")
    .size()
)

print("\nSequence Length Statistics:")
print(sequence_lengths.describe())

# Check negative values
numeric_cols = flight_df.select_dtypes(include=np.number).columns

print("\nNegative Value Check:")

for col in numeric_cols:
    negatives = (flight_df[col] < 0).sum()

    if negatives > 0:
        print(f"{col}: {negatives} negative values")

# LOYALTY HISTORY CHECKS
print("\n" + "="*80)
print("LOYALTY HISTORY DEEP CHECKS")
print("="*80)

# Unique customers
print("\nUnique Customers:")
print(loyalty_df["Loyalty Number"].nunique())

# Cancellation distribution
if "Cancellation Year" in loyalty_df.columns:

    print("\nCancellation Distribution:")
    print(
        loyalty_df["Cancellation Year"]
        .value_counts(dropna=False)
        .sort_index()
    )

# CLV statistics
if "CLV" in loyalty_df.columns:

    print("\nCLV Statistics:")
    print(loyalty_df["CLV"].describe())

# Loyalty card distribution
if "Loyalty Card" in loyalty_df.columns:

    print("\nLoyalty Card Distribution:")
    print(loyalty_df["Loyalty Card"].value_counts())

# CUSTOMER OVERLAP CHECK
print("\n" + "="*80)
print("CUSTOMER OVERLAP CHECK")
print("="*80)

flight_customers = set(flight_df["Loyalty Number"].unique())
loyalty_customers = set(loyalty_df["Loyalty Number"].unique())

common_customers = flight_customers.intersection(loyalty_customers)

print(f"\nCustomers in Flight Activity: {len(flight_customers)}")
print(f"Customers in Loyalty History: {len(loyalty_customers)}")
print(f"Common Customers: {len(common_customers)}")

# POSSIBLE LEAKAGE CHECK
print("\n" + "="*80)
print("POTENTIAL LEAKAGE CHECK")
print("="*80)

possible_leakage_keywords = [
    "cancel",
    "churn",
    "future",
    "target",
    "label"
]

for col in loyalty_df.columns:

    lower_col = col.lower()

    for keyword in possible_leakage_keywords:

        if keyword in lower_col:
            print(f"Potential leakage column: {col}")
            
dup = flight_df[
    flight_df.duplicated(
        subset=["Loyalty Number", "Year", "Month"],
        keep=False
    )
]

print("Duplicate customer-month rows:")
print(len(dup))

print("\nExamples:")
print(
    dup.sort_values(
        ["Loyalty Number","Year","Month"]
    ).head(20)
)

print("\nZero Flight Months:")
print((flight_df["Total Flights"] == 0).sum())

print("\nPercentage:")
print(
    round(
        (flight_df["Total Flights"] == 0).mean()*100,
        2
    ),
    "%"
)

customer_stats = (
    flight_df
    .groupby("Loyalty Number")
    ["Total Flights"]
    .agg([
        "sum",
        "mean",
        "std",
        "max"
    ])
)

print(customer_stats.describe())

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

print(monthly_df.shape)

print(
    monthly_df.head()
)

print(
    "\nDuplicate customer-month rows:",
    monthly_df.duplicated(
        subset=["Loyalty Number","Year","Month"]
    ).sum()
)

seq_lengths = (
    monthly_df
    .groupby("Loyalty Number")
    .size()
)

print(seq_lengths.describe())

import pandas as pd

monthly_df = monthly_df.sort_values(
    ["Loyalty Number", "Year", "Month"]
)

def max_zero_streak(series):
    max_streak = 0
    current = 0

    for x in series:
        if x == 0:
            current += 1
            max_streak = max(max_streak, current)
        else:
            current = 0

    return max_streak

streaks = (
    monthly_df
    .groupby("Loyalty Number")["Total Flights"]
    .apply(max_zero_streak)
)

print(streaks.describe())

print("\nCustomers with >=3 month inactivity:")
print((streaks >= 3).sum())

print("\nCustomers with >=4 month inactivity:")
print((streaks >= 4).sum())

print("\nCustomers with >=5 month inactivity:")
print((streaks >= 5).sum())

print("\nCustomers with >=6 month inactivity:")
print((streaks >= 6).sum())

# Create inactivity streak table
streak_df = streaks.reset_index()
streak_df.columns = ["Loyalty Number", "Max_Inactive_Streak"]

# Merge with loyalty history
merged = streak_df.merge(
    loyalty_df[
        ["Loyalty Number", "Cancellation Year"]
    ],
    on="Loyalty Number",
    how="left"
)

merged["Cancelled"] = (
    merged["Cancellation Year"]
    .notna()
    .astype(int)
)

for threshold in [3,4,5,6,7,8,9,10]:
    
    subset = merged[
        merged["Max_Inactive_Streak"] >= threshold
    ]
    
    cancel_rate = subset["Cancelled"].mean()

    print(
        f"Threshold {threshold}: "
        f"{len(subset)} customers, "
        f"Cancellation Rate = {cancel_rate:.3f}"
    )

merged_df = monthly_df.groupby("Loyalty Number").agg({
    "Total Flights":"sum",
    "Distance":"sum",
    "Points Accumulated":"sum",
    "Points Redeemed":"sum"
}).reset_index()

merged_df = merged_df.merge(
    loyalty_df,
    on="Loyalty Number"
)

print(
    merged_df[
        ["CLV",
         "Total Flights",
         "Distance",
         "Points Accumulated",
         "Points Redeemed"]
    ].corr(numeric_only=True)
)