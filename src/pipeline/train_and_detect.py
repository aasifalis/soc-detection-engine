# src/pipeline/train_and_detect.py

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

print("File is running")

# Import your generator
from src.data.generator import generate_full_dataset


def run_pipeline():
    
    
    print("Pipeline started")

    # 1️⃣ Generate dataset
    df = generate_full_dataset()

    # 2️⃣ Split baseline vs detection
    baseline_df = df[df["window"] == "baseline"]
    detection_df = df[df["window"] == "detection"]

    # 3️⃣ Select feature columns
    feature_cols = [
        col for col in df.columns
        if col not in ["ip", "window"]
    ]

    X_baseline = baseline_df[feature_cols]
    X_detection = detection_df[feature_cols]

    # 4️⃣ Scale (fit on baseline only)
    scaler = StandardScaler()
    X_baseline_scaled = scaler.fit_transform(X_baseline)
    X_detection_scaled = scaler.transform(X_detection)

    # 5️⃣ Train Isolation Forest
    model = IsolationForest(
        contamination=0.1,
        random_state=42
    )

    model.fit(X_baseline_scaled)

    # 6️⃣ Score detection window
    scores = -model.decision_function(X_detection_scaled)
    predictions = model.predict(X_detection_scaled)

    detection_df = detection_df.copy()
    detection_df["anomaly_score"] = scores
    detection_df["is_anomaly"] = (predictions == -1).astype(int)

    # 7️⃣ Rank results
    ranked = detection_df.sort_values(
        "anomaly_score",
        ascending=False
    )

    print("\nTop 20 Most Suspicious IPs:\n")
    print(ranked[["ip", "anomaly_score", "is_anomaly"]].head(20))

    # ==============================
    # 🔎 Evaluation Metrics Section
    # ==============================

    # Ground truth (synthetic attackers)
    detection_df["is_attacker"] = detection_df["ip"].str.contains("ATTACK").astype(int)

    total_attackers = detection_df["is_attacker"].sum()
    total_normals = len(detection_df) - total_attackers

    true_positives = detection_df[
        (detection_df["is_attacker"] == 1) &
        (detection_df["is_anomaly"] == 1)
    ].shape[0]

    false_positives = detection_df[
        (detection_df["is_attacker"] == 0) &
        (detection_df["is_anomaly"] == 1)
    ].shape[0]

    recall = true_positives / total_attackers if total_attackers > 0 else 0
    false_positive_rate = false_positives / total_normals if total_normals > 0 else 0

    print("\n--- Evaluation Metrics ---")
    print(f"Total Attackers: {total_attackers}")
    print(f"Total Normals: {total_normals}")
    print(f"True Positives: {true_positives}")
    print(f"False Positives: {false_positives}")
    print(f"Recall (Detection Rate): {recall:.2f}")
    print(f"False Positive Rate: {false_positive_rate:.2f}")

    print("\nDataset Shape:", df.shape)


if __name__ == "__main__":
    run_pipeline()