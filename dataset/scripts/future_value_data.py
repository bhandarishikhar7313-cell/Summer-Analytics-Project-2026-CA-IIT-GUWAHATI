import numpy as np
import pandas as pd

from pathlib import Path


# PATHS
BASE_DIR = Path(__file__).parent.parent

CSV_DIR = BASE_DIR / "graphs" / "csv"

TENSOR_DIR = BASE_DIR / "graphs" / "tensors_csv"

TENSOR_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# LOAD DATA
sequence_df = pd.read_csv(
    CSV_DIR / "sequence_dataset.csv"
)

sequence_df["date"] = pd.to_datetime(
    sequence_df["date"]
)

sequence_df = sequence_df.sort_values(
    ["Loyalty Number", "date"]
)

print(
    "Sequence Shape:",
    sequence_df.shape
)

# BUILD TARGETS
customer_ids = sorted(
    sequence_df["Loyalty Number"].unique()
)

y_future = []

valid_count = 0
skip_count = 0

for customer_id in customer_ids:

    customer_data = sequence_df[
        sequence_df["Loyalty Number"]
        == customer_id
    ]

    past_window = customer_data[
        customer_data["date"]
        < "2018-01-01"
    ]

    if len(past_window) != 12:

        skip_count += 1
        continue

    future_window = customer_data[
        (
            customer_data["date"]
            >= "2018-01-01"
        )
        &
        (
            customer_data["date"]
            <= "2018-06-30"
        )
    ]

    future_flights = future_window[
        "Total Flights"
    ].sum()

    future_distance = future_window[
        "Distance"
    ].sum()

    future_points = future_window[
        "Points Accumulated"
    ].sum()

    y_future.append(

        [
            future_flights,
            future_distance,
            future_points
        ]

    )

    valid_count += 1

# CONVERT
y_future = np.array(
    y_future,
    dtype=np.float32
)

# SAVE
np.save(

    TENSOR_DIR
    / "y_future.npy",

    y_future

)

# STATS
print("\nCustomers Used:", valid_count)

print("Customers Skipped:", skip_count)

print(
    "\ny_future Shape:",
    y_future.shape
)

print(
    "\nExample Target:"
)

print(
    y_future[0]
)

print(
    "\nFuture Flights Mean:",
    round(
        y_future[:,0].mean(),
        2
    )
)

print(
    "Future Distance Mean:",
    round(
        y_future[:,1].mean(),
        2
    )
)

print(
    "Future Points Mean:",
    round(
        y_future[:,2].mean(),
        2
    )
)

targets = [
    "Flights",
    "Distance",
    "Points"
]

for i, name in enumerate(targets):

    print(f"\n{name}")

    print(
        pd.Series(
            y_future[:, i]
        ).describe()
    )

print(
    "\nSaved:"
)

print(
    TENSOR_DIR
    / "y_future.npy"
)