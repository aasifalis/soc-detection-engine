import re
import pandas as pd


def parse_apache_logs(file_path):
    data = []

    pattern = r'(\d+\.\d+\.\d+\.\d+).*\[(.*?)\] "(GET|POST) (.*?) HTTP.*?" (\d{3})'

    with open(file_path, "r") as file:
        for line in file:
            match = re.search(pattern, line)

            if match:
                ip, timestamp, method, endpoint, status = match.groups()

                data.append({
                    "source": "apache",
                    "ip": ip,
                    "timestamp": timestamp,
                    "method": method,
                    "endpoint": endpoint,
                    "status_code": int(status),
                    "raw_log": line.strip()
                })

    return pd.DataFrame(data)