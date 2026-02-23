import pandas as pd
from parsers.ssh_parser import parse_ssh_logs


def test_ssh_parser_basic(tmp_path):
    log_content = (
        "Failed password for root from 185.23.45.12 port 22 ssh2\n"
        "Accepted password for user from 192.168.1.5 port 22 ssh2\n"
    )

    file = tmp_path / "test_ssh.log"
    file.write_text(log_content)

    df = parse_ssh_logs(file)

    assert len(df) == 2
    assert df.iloc[0]["ip"] == "185.23.45.12"
    assert df.iloc[0]["failed_login"] == 1
    assert df.iloc[1]["failed_login"] == 0