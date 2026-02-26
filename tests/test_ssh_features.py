import pandas as pd
from feature_engineering.ssh_features import aggregate_ssh_features
import pandas as pd

def test_ssh_basic_aggregation():
    data = pd.DataFrame({
        "ip": ["A", "A", "A", "B"],
        "username": ["root", "admin", "root", "user"],
        "failed_login": [1, 1, 0, 0],
    })

    result = aggregate_ssh_features(data)

    # IP A
    ip_a = result[result["ip"] == "A"].iloc[0]
    assert ip_a["ssh_total_attempts"] == 3
    assert ip_a["ssh_failed_attempts"] == 2
    assert ip_a["ssh_success_attempts"] == 1
    assert ip_a["ssh_unique_usernames"] == 2
    assert ip_a["ssh_failure_ratio"] == 2 / 3

    # IP B
    ip_b = result[result["ip"] == "B"].iloc[0]
    assert ip_b["ssh_total_attempts"] == 1
    assert ip_b["ssh_failed_attempts"] == 0
    assert ip_b["ssh_failure_ratio"] == 0.0

def test_ssh_empty_input():
    empty_df = pd.DataFrame(columns=["ip", "username", "failed_login"])
    result = aggregate_ssh_features(empty_df)

    assert result.empty