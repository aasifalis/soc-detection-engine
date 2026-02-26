from feature_engineering.web_features import aggregate_web_features
import pandas as pd
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