import re
import pandas as pd


def parse_ssh_logs(file_path):
    data = []

    ip_pattern = r'(\d+\.\d+\.\d+\.\d+)'
    user_pattern = r'for (\w+)'

    with open(file_path, "r") as file:
        for line in file:
            ip_match = re.search(ip_pattern, line)
            user_match = re.search(user_pattern, line)

            if ip_match:
                data.append({
                    "source": "ssh",
                    "ip": ip_match.group(1),
                    "username": user_match.group(1) if user_match else None,
                    "failed_login": int("Failed" in line),
                    "raw_log": line.strip()
                })

    return pd.DataFrame(data)