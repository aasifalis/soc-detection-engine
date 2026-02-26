import pandas as pd


def aggregate_ssh_features(df: pd.DataFrame) -> pd.DataFrame:

    if df.empty:
        return pd.DataFrame()

    grouped = df.groupby("ip")

    features = grouped.agg(
        ssh_total_attempts=("failed_login", "count"),
        ssh_failed_attempts=("failed_login", "sum"),
        ssh_unique_usernames=("username", "nunique"),
    ).reset_index()

    features["ssh_success_attempts"] = (
        features["ssh_total_attempts"] - features["ssh_failed_attempts"]
    )

    features["ssh_failure_ratio"] = (
        features["ssh_failed_attempts"] / features["ssh_total_attempts"]
    )

    return features