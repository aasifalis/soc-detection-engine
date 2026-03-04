from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import pandas as pd

from src.data.generator import generate_full_dataset


def run_isolation_forest(contamination: float = 0.15):

    df = generate_full_dataset()

    X = df.drop(columns=["ip"])

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)


    model = IsolationForest(
        contamination=contamination,
        random_state=42
    )

    model.fit(X_scaled)
    
    anomaly_scores = -model.decision_function(X_scaled)

    predictions = model.predict(X_scaled)
    is_anomaly = (predictions == -1).astype(int)

    df["anomaly_score"] = anomaly_scores
    df["is_anomaly"] = is_anomaly

    ranked = df.sort_values("anomaly_score", ascending=False)

    return ranked


if __name__ == "__main__":

    results = run_isolation_forest(contamination=0.15)

    print("\nTop 20 Most Suspicious IPs:\n")
    print(results[["ip", "anomaly_score", "is_anomaly"]].head(20))

    print("\nDataset Shape:", results.shape)