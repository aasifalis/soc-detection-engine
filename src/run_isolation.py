from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import pandas as pd

from src.data.generator import generate_full_dataset


def run_isolation_forest(contamination: float = 0.3):

    # Generate dataset
    df = generate_full_dataset()

    # Remove non-feature column
    X = df.drop(columns=["ip"])

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train Isolation Forest
    model = IsolationForest(
        contamination=contamination,   # use function parameter
        random_state=42
    )

    model.fit(X_scaled)

    # Compute anomaly scores
    anomaly_scores = -model.decision_function(X_scaled)

    # Predict anomalies
    predictions = model.predict(X_scaled)
    is_anomaly = (predictions == -1).astype(int)

    # Add results to dataframe
    df["anomaly_score"] = anomaly_scores
    df["is_anomaly"] = is_anomaly

    # Rank suspicious IPs
    ranked = df.sort_values("anomaly_score", ascending=False)

    return ranked


if __name__ == "__main__":

    results = run_isolation_forest(contamination=0.3)

    print("\nTop 20 Most Suspicious IPs:\n")
    print(results[["ip", "anomaly_score", "is_anomaly"]].head(20))

    print("\nDataset Shape:", results.shape)