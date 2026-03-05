import os
from typing import List

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from src.data.cicids_loader import load_cicids_dataset
from src.data.generator import generate_full_dataset


USE_CICIDS = True


def _print_metrics(df: pd.DataFrame) -> None:
    total_attackers = int(df["is_attacker"].sum())
    total_normals = len(df) - total_attackers

    true_positives = int(
        df[(df["is_attacker"] == 1) & (df["is_anomaly"] == 1)].shape[0]
    )
    false_positives = int(
        df[(df["is_attacker"] == 0) & (df["is_anomaly"] == 1)].shape[0]
    )

    recall = true_positives / total_attackers if total_attackers > 0 else 0.0
    false_positive_rate = (
        false_positives / total_normals if total_normals > 0 else 0.0
    )

    print("\n--- Evaluation Metrics ---")
    print(f"Total Attackers: {total_attackers}")
    print(f"Total Normals: {total_normals}")
    print(f"True Positives: {true_positives}")
    print(f"False Positives: {false_positives}")
    print(f"Recall (Detection Rate): {recall:.2f}")
    print(f"False Positive Rate: {false_positive_rate:.2f}")


def _train_and_detect(
    X_train: np.ndarray, X_test: np.ndarray, df_out: pd.DataFrame, id_cols: List[str]
) -> pd.DataFrame:
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = IsolationForest(contamination=0.15, random_state=42)
    model.fit(X_train_scaled)

    scores = -model.decision_function(X_test_scaled)
    predictions = model.predict(X_test_scaled)

    out = df_out.copy()
    out["anomaly_score"] = scores
    out["is_anomaly"] = (predictions == -1).astype(int)

    ranked = out.sort_values("anomaly_score", ascending=False)
    display_cols = id_cols + ["anomaly_score", "is_anomaly"]
    print(ranked[display_cols].head(20))

    return out


def run_pipeline() -> None:
    print("Pipeline started")

    if USE_CICIDS:
        print("Loading CICIDS dataset...")
        df = load_cicids_dataset("src/data/cicids/portscan.csv")
        df["is_attacker"] = (df["Label"] != "BENIGN").astype(int)

        feature_cols = [
            "Flow Duration",
            "Total Fwd Packets",
            "Total Backward Packets",
            "Total Length of Fwd Packets",
            "Total Length of Bwd Packets",
            "Flow Bytes/s",
            "Flow Packets/s",
            "Packet Length Mean",
            "Packet Length Std",
            "SYN Flag Count",
            "ACK Flag Count",
            "RST Flag Count",
        ]

        train_df = df[df["Label"] == "BENIGN"]
        test_df = df

        X_train = train_df[feature_cols]
        X_test = test_df[feature_cols]

        result_df = _train_and_detect(
            X_train.values, X_test.values, test_df, id_cols=["Label"]
        )

        _print_metrics(result_df)
        print("\nDataset Shape:", result_df.shape)

    else:
        print("Loading synthetic dataset...")
        df = generate_full_dataset()

        baseline_df = df[df["window"] == "baseline"]
        detection_df = df[df["window"] == "detection"]

        feature_cols = [col for col in df.columns if col not in ["ip", "window"]]

        X_baseline = baseline_df[feature_cols]
        X_detection = detection_df[feature_cols]

        result_df = _train_and_detect(
            X_baseline.values, X_detection.values, detection_df, id_cols=["ip"]
        )

        result_df["is_attacker"] = result_df["ip"].str.contains("ATTACK").astype(int)
        _print_metrics(result_df)
        print("\nDataset Shape:", result_df.shape)


if __name__ == "__main__":
    run_pipeline()