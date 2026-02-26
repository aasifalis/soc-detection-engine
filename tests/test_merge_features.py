import pandas as pd
from feature_engineering.ssh_features import aggregate_ssh_features
from feature_engineering.web_features import aggregate_web_features
from feature_engineering.merge_features import (
    merge_feature_tables,
    compute_global_features
)

def test_ssh_basic_aggregation():
    data = pd.DataFrame({
        "ip": ["A", "A", "A", "B"],
        "username": ["root", "admin", "root", "user"],
        "failed_login": [1, 1, 0, 0],
    })

    result = aggregate_ssh_features(data)

    ip_a = result[result["ip"] == "A"].iloc[0]
    assert ip_a["ssh_total_attempts"] == 3
    assert ip_a["ssh_failed_attempts"] == 2
    assert ip_a["ssh_success_attempts"] == 1
    assert ip_a["ssh_unique_usernames"] == 2
    assert ip_a["ssh_failure_ratio"] == 2 / 3

    ip_b = result[result["ip"] == "B"].iloc[0]
    assert ip_b["ssh_total_attempts"] == 1
    assert ip_b["ssh_failed_attempts"] == 0
    assert ip_b["ssh_failure_ratio"] == 0.0


def test_ssh_empty_input():
    empty_df = pd.DataFrame(columns=["ip", "username", "failed_login"])
    result = aggregate_ssh_features(empty_df)
    assert result.empty

def test_web_basic_aggregation():
    data = pd.DataFrame({
        "ip": ["A", "A", "A", "B"],
        "method": ["GET", "POST", "GET", "POST"],
        "endpoint": ["/home", "/login", "/admin", "/login"],
        "status_code": [200, 404, 500, 200],
    })

    result = aggregate_web_features(data)

    ip_a = result[result["ip"] == "A"].iloc[0]

    assert ip_a["web_total_requests"] == 3
    assert ip_a["web_error_responses"] == 2
    assert ip_a["web_post_requests"] == 1
    assert ip_a["web_unique_endpoints"] == 3
    assert ip_a["web_error_ratio"] == 2 / 3
    assert ip_a["web_post_ratio"] == 1 / 3


def test_web_empty_input():
    empty_df = pd.DataFrame(columns=["ip", "method", "endpoint", "status_code"])
    result = aggregate_web_features(empty_df)
    assert result.empty

def test_merge_with_overlapping_ips():
    ssh_df = pd.DataFrame({
        "ip": ["A", "B"],
        "ssh_total_attempts": [10, 5],
        "ssh_failed_attempts": [7, 1],
    })

    web_df = pd.DataFrame({
        "ip": ["A", "C"],
        "web_total_requests": [20, 15],
        "web_error_responses": [5, 3],
    })

    merged = merge_feature_tables(ssh_df, web_df)

    assert set(merged["ip"]) == {"A", "B", "C"}

    ip_a = merged[merged["ip"] == "A"].iloc[0]
    assert ip_a["ssh_total_attempts"] == 10
    assert ip_a["web_total_requests"] == 20

    ip_b = merged[merged["ip"] == "B"].iloc[0]
    assert ip_b["web_total_requests"] == 0

    ip_c = merged[merged["ip"] == "C"].iloc[0]
    assert ip_c["ssh_total_attempts"] == 0


def test_compute_global_features():
    df = pd.DataFrame({
        "ip": ["A", "B"],
        "ssh_total_attempts": [10, 0],
        "web_total_requests": [20, 5],
    })

    result = compute_global_features(df)

    ip_a = result[result["ip"] == "A"].iloc[0]
    ip_b = result[result["ip"] == "B"].iloc[0]

    assert ip_a["seen_in_ssh"] == 1
    assert ip_a["seen_in_web"] == 1
    assert ip_a["total_activity"] == 30
    assert ip_a["ssh_activity_ratio"] == 10 / 30

    assert ip_b["seen_in_ssh"] == 0
    assert ip_b["seen_in_web"] == 1
    assert ip_b["total_activity"] == 5
    assert ip_b["ssh_activity_ratio"] == 0


def test_merge_empty_inputs():
    ssh_df = pd.DataFrame()
    web_df = pd.DataFrame()

    merged = merge_feature_tables(ssh_df, web_df)
    assert merged.empty