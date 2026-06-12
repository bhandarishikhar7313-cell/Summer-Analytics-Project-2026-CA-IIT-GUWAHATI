import pandas as pd

labels = pd.read_csv(
    r"C:\shikhar(D drive)\D drive\Personal\iit\dataset\graphs\csv\training_labels.csv"
)

print(labels.head())

print("\nColumns:")
print(labels.columns.tolist())

print("\nChurn Distribution:")
print(labels["churn"].value_counts())