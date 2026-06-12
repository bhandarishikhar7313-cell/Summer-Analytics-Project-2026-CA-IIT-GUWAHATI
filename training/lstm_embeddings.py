import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

import tensorflow as tf

print(tf.__version__)

from tensorflow.keras.models import Model # type: ignore
from tensorflow.keras.layers import ( # type: ignore
    Input,
    LSTM,
    Dense,
    Dropout
)

from tensorflow.keras.callbacks import ( # type: ignore
    EarlyStopping,
    ReduceLROnPlateau,
    ModelCheckpoint
)

# PATHS
PROJECT_DIR = Path(__file__).resolve().parent.parent

DATASET_DIR = PROJECT_DIR / "dataset"

TENSOR_DIR = (
    DATASET_DIR
    / "graphs"
    / "tensors_csv"
)

OUTPUT_DIR = (
    DATASET_DIR
    / "graphs"
    / "lstm_encoder"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# LOAD DATA
X_seq = np.load(
    TENSOR_DIR / "X_seq_forecast.npy"
)

y = np.load(
    TENSOR_DIR / "y_forecast.npy"
)

print("X_seq Shape:", X_seq.shape)
print("y Shape:", y.shape)

# SCALE SEQUENCES
num_samples = X_seq.shape[0]

X_flat = X_seq.reshape(
    -1,
    X_seq.shape[-1]
)



mean = X_flat.mean(axis=0)

std = X_flat.std(axis=0)

X_flat = (
    X_flat - mean
) / (std + 1e-8)

X_seq = X_flat.reshape(
    X_seq.shape
)

# SAVE NORMALIZATION STATS
np.save(
    OUTPUT_DIR / "sequence_mean.npy",
    mean
)

np.save(
    OUTPUT_DIR / "sequence_std.npy",
    std
)

print("\nSaved:")
print("sequence_mean.npy")
print("sequence_std.npy")

# SPLIT
X_train, X_val, y_train, y_val = train_test_split(

    X_seq,
    y,

    test_size=0.20,

    stratify=y,

    random_state=42

)

print("\nTrain:", X_train.shape)
print("Val:", X_val.shape)

# MODEL
inputs = Input(
    shape=(12, 5)
)

x = LSTM(
    64,
    return_sequences=False,
    name="encoder_lstm"
)(inputs)

embedding = Dense(
    32,
    activation="relu",
    name="behavior_embedding"
)(x)

x = Dropout(0.3)(
    embedding
)

outputs = Dense(
    1,
    activation="sigmoid"
)(x)

model = Model(
    inputs,
    outputs
)

model.compile(

    optimizer="adam",

    loss="binary_crossentropy",

    metrics=[
        "accuracy"
    ]
)

model.summary()

# CALLBACKS
callbacks = [

    EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True
    ),

    ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,
        patience=2
    ),

    ModelCheckpoint(
        OUTPUT_DIR / "best_lstm.keras",
        save_best_only=True
    )

]

# TRAIN
history = model.fit(

    X_train,
    y_train,

    validation_data=(
        X_val,
        y_val
    ),

    epochs=50,

    batch_size=128,

    callbacks=callbacks,

    verbose=1
)

# EVALUATION
y_prob = model.predict(
    X_val
).flatten()

y_pred = (
    y_prob > 0.5
).astype(int)

acc = accuracy_score(
    y_val,
    y_pred
)

prec = precision_score(
    y_val,
    y_pred
)

rec = recall_score(
    y_val,
    y_pred
)

f1 = f1_score(
    y_val,
    y_pred
)

auc = roc_auc_score(
    y_val,
    y_prob
)

print("\n==========================")
print("Accuracy :", acc)
print("Precision:", prec)
print("Recall   :", rec)
print("F1       :", f1)
print("ROC AUC  :", auc)
print("==========================")

# SAVE CURVES
plt.figure(figsize=(8,5))

plt.plot(
    history.history["loss"],
    label="train"
)

plt.plot(
    history.history["val_loss"],
    label="val"
)

plt.legend()

plt.title("Loss")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "loss_curve.png",
    dpi=300
)

plt.close()

# EMBEDDING MODEL
embedding_model = Model(

    inputs=model.input,

    outputs=model.get_layer(
        "behavior_embedding"
    ).output

)

embeddings = embedding_model.predict(
    X_seq,
    batch_size=512
)

print(
    "\nEmbedding Shape:",
    embeddings.shape
)

np.save(

    OUTPUT_DIR
    / "behavior_embeddings.npy",

    embeddings

)

# SAVE FULL MODELS
model.save(
    OUTPUT_DIR / "full_lstm_model.keras"
)

embedding_model.save(
    OUTPUT_DIR / "embedding_model.keras"
)

print("\nSaved Models:")
print("full_lstm_model.keras")
print("embedding_model.keras")

print(
    "\nSaved behavior_embeddings.npy"
)