from parsers.apache_parser import parse_apache_logs


def test_apache_parser_basic(tmp_path):
    log_content = (
        "192.168.1.1 - - [21/Feb/2026:10:32:45 +0000] \"GET /login HTTP/1.1\" 200 512\n"
        "203.54.1.99 - - [21/Feb/2026:10:35:21 +0000] \"POST /admin HTTP/1.1\" 404 210\n"
    )

    file = tmp_path / "test_apache.log"
    file.write_text(log_content)

    df = parse_apache_logs(file)

    assert len(df) == 2
    assert df.iloc[0]["ip"] == "192.168.1.1"
    assert df.iloc[1]["method"] == "POST"
    assert df.iloc[1]["status_code"] == 404