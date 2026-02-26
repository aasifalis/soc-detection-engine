import pandas as pd


def aggregate_web_features(df: pd.DataFrame) -> pd.DataFrame:


    if df.empty:
        return pd.DataFrame()

    df = df.copy()
    df["is_error"] = (df["status_code"] >= 400).astype(int)
    df["is_post"] = (df["method"] == "POST").astype(int)

    grouped = df.groupby("ip")

    features = grouped.agg(
        web_total_requests=("status_code", "count"),
        web_error_responses=("is_error", "sum"),
        web_post_requests=("is_post", "sum"),
        web_unique_endpoints=("endpoint", "nunique"),
    ).reset_index()

    features["web_error_ratio"] = (
        features["web_error_responses"] /
        features["web_total_requests"]
    )

    features["web_post_ratio"] = (
        features["web_post_requests"] /
        features["web_total_requests"]
    )

    return features