import platform
import scanner_12a

def test_scan_bastion(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    # Run scan
    scanner_12a.scan_bastion()
    captured = capsys.readouterr()

    assert "--- [ SCANNER DE SOUVERAINETÉ 12_ALPHA ] ---" in captured.out

    expected_log_file = tmp_path / "DATA" / "LOGS_SOUVERAINS" / "session_log.txt"
    assert expected_log_file.exists()

    with open(expected_log_file, "r") as f:
        content = f.read()
    assert "Scan de souveraineté effectué. État : ALIGNÉ." in content

def test_scan_bastion_darwin(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(platform, "mac_ver", lambda: ("14.2.1", ("", "", ""), ""))

    scanner_12a.scan_bastion()
    captured = capsys.readouterr()

    assert "OS VERSION : macOS 14.2.1" in captured.out
