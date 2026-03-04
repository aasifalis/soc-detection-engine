import pandas as pd
import numpy as np


def generate_normal_behaviour(n=200):
    """
    Generate normal user behaviour.
    """
    data = []

    for i in range(n):
        ssh_total = np.random.poisson(3)
        ssh_failed = np.random.binomial(ssh_total, 0.2) if ssh_total > 0 else 0

        web_total = np.random.poisson(20)
        web_errors = np.random.binomial(web_total, 0.05) if web_total > 0 else 0

        row = {
            "ip": f"NORMAL_{i}",
            "ssh_total_attempts": ssh_total,
            "ssh_failed_attempts": ssh_failed,
            "ssh_success_attempts": ssh_total - ssh_failed,
            "ssh_failure_ratio": ssh_failed / ssh_total if ssh_total > 0 else 0,
            "ssh_unique_usernames": np.random.randint(1, 3),

            "web_total_requests": web_total,
            "web_error_responses": web_errors,
            "web_post_requests": np.random.binomial(web_total, 0.1),
            "web_unique_endpoints": np.random.randint(3, 10),
            "web_error_ratio": web_errors / web_total if web_total > 0 else 0,
            "web_post_ratio": np.random.uniform(0.05, 0.2),

            "seen_in_ssh": int(ssh_total > 0),
            "seen_in_web": int(web_total > 0),
        }

        data.append(row)

    df = pd.DataFrame(data)
    df["total_activity"] = df["ssh_total_attempts"] + df["web_total_requests"]
    df["ssh_activity_ratio"] = (
        df["ssh_total_attempts"] / df["total_activity"]
    ).fillna(0)

    return df


def generate_ssh_bruteforce(n=20):
    """
    Generate SSH brute force attackers.
    """
    data = []

    for i in range(n):
        ssh_total = np.random.randint(100, 400)
        ssh_failed = int(ssh_total * np.random.uniform(0.9, 0.99))

        web_total = np.random.randint(0, 10)

        row = {
            "ip": f"SSH_ATTACK_{i}",
            "ssh_total_attempts": ssh_total,
            "ssh_failed_attempts": ssh_failed,
            "ssh_success_attempts": ssh_total - ssh_failed,
            "ssh_failure_ratio": ssh_failed / ssh_total,
            "ssh_unique_usernames": np.random.randint(10, 50),

            "web_total_requests": web_total,
            "web_error_responses": 0,
            "web_post_requests": 0,
            "web_unique_endpoints": 1,
            "web_error_ratio": 0,
            "web_post_ratio": 0,

            "seen_in_ssh": 1,
            "seen_in_web": int(web_total > 0),
        }

        data.append(row)

    df = pd.DataFrame(data)
    df["total_activity"] = df["ssh_total_attempts"] + df["web_total_requests"]
    df["ssh_activity_ratio"] = (
        df["ssh_total_attempts"] / df["total_activity"]
    )

    return df


def generate_web_scanner(n=20):
    """
    Generate web scanning attackers.
    """
    data = []

    for i in range(n):
        web_total = np.random.randint(200, 600)
        web_errors = int(web_total * np.random.uniform(0.6, 0.9))

        row = {
            "ip": f"WEB_ATTACK_{i}",
            "ssh_total_attempts": 0,
            "ssh_failed_attempts": 0,
            "ssh_success_attempts": 0,
            "ssh_failure_ratio": 0,
            "ssh_unique_usernames": 0,

            "web_total_requests": web_total,
            "web_error_responses": web_errors,
            "web_post_requests": np.random.randint(50, 200),
            "web_unique_endpoints": np.random.randint(100, 300),
            "web_error_ratio": web_errors / web_total,
            "web_post_ratio": np.random.uniform(0.5, 0.9),

            "seen_in_ssh": 0,
            "seen_in_web": 1,
        }

        data.append(row)

    df = pd.DataFrame(data)
    df["total_activity"] = df["web_total_requests"]
    df["ssh_activity_ratio"] = 0

    return df


def generate_full_dataset():
    """
    Generate dataset with baseline vs detection window split.
    """

    # --- Baseline Window ---
    baseline_normal = generate_normal_behaviour(180)
    baseline_ssh = generate_ssh_bruteforce(3)
    baseline_web = generate_web_scanner(3)

    baseline_df = pd.concat(
        [baseline_normal, baseline_ssh, baseline_web]
    ).reset_index(drop=True)

    baseline_df["window"] = "baseline"

    # --- Detection Window ---
    detection_normal = generate_normal_behaviour(20)
    detection_ssh = generate_ssh_bruteforce(17)
    detection_web = generate_web_scanner(17)

    detection_df = pd.concat(
        [detection_normal, detection_ssh, detection_web]
    ).reset_index(drop=True)

    detection_df["window"] = "detection"

    # Combine
    full_df = pd.concat([baseline_df, detection_df]).reset_index(drop=True)

    return full_df