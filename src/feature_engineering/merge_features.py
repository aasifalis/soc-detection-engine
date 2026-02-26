import pandas as pd


def merge_feature_tables(ssh_df: pd.DataFrame,
                         web_df: pd.DataFrame) -> pd.DataFrame:

    if ssh_df.empty and web_df.empty:
        return pd.DataFrame()

    merged = pd.merge(
        ssh_df,
        web_df,
        on="ip",
        how="outer"
    )

    merged = merged.fillna(0)

    return merged


def compute_global_features(df: pd.DataFrame) -> pd.DataFrame:

    if df.empty:
        return df

    df = df.copy()

    df["seen_in_ssh"] = (df.get("ssh_total_attempts", 0) > 0).astype(int)
    df["seen_in_web"] = (df.get("web_total_requests", 0) > 0).astype(int)

    df["total_activity"] = (
        df.get("ssh_total_attempts", 0) +
        df.get("web_total_requests", 0)
    )

    df["ssh_activity_ratio"] = 0.0

    mask = df["total_activity"] > 0
    df.loc[mask, "ssh_activity_ratio"] = (
        df.loc[mask, "ssh_total_attempts"] /
        df.loc[mask, "total_activity"]
    )

    return df