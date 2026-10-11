import scanner_12a

def test_scan_bastion_non_darwin(tmp_path, monkeypatch, capsys):
    # Set current working directory to a tmp path with fake git and config
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".git").mkdir()
    data_dir = tmp_path / "DATA"
    data_dir.mkdir()
    (data_dir / "config_anastasia.json").write_text("{}")

    monkeypatch.setattr("platform.system", lambda: "Linux")

    # Ensure platform.mac_ver is not called on non-Darwin or returns empty
    mac_ver_called = []
    def fake_mac_ver():
        mac_ver_called.append(True)
        return ("14.0", ("", "", ""), "")
    monkeypatch.setattr("platform.mac_ver", fake_mac_ver)

    scanner_12a.scan_bastion()

    captured = capsys.readouterr()
    assert "--- [ SCANNER DE SOUVERAINETÉ 12_ALPHA ] ---" in captured.out
    assert "OS VERSION : macOS " in captured.out
    assert "ÉTAT       : BASTION VERROUILLÉ ET ALIGNÉ ✅" in captured.out
    assert mac_ver_called == [], "platform.mac_ver() should not be called when system is Linux"

    log_file = tmp_path / "DATA" / "LOGS_SOUVERAINS" / "session_log.txt"
    assert log_file.exists()
    content = log_file.read_text()
    assert "Scan de souveraineté effectué. État : ALIGNÉ." in content

def test_scan_bastion_darwin(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("platform.system", lambda: "Darwin")

    mac_ver_called = []
    def fake_mac_ver():
        mac_ver_called.append(True)
        return ("14.2.1", ("", "", ""), "")
    monkeypatch.setattr("platform.mac_ver", fake_mac_ver)

    scanner_12a.scan_bastion()

    captured = capsys.readouterr()
    assert "OS VERSION : macOS 14.2.1" in captured.out
    assert mac_ver_called == [True], "platform.mac_ver() should be called when system is Darwin"
    assert "ÉTAT       : DÉSYNCHRONISATION DÉTECTÉE ⚠️" in captured.out
