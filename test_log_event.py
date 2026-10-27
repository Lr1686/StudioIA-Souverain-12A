import log_event

def test_enregistrer_evenement(tmp_path, monkeypatch, capsys):
    # Change working directory to tmp_path to test directory creation and file writing
    monkeypatch.chdir(tmp_path)

    log_event.enregistrer_evenement("Test Message 1")
    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test Message 1" in captured.out

    expected_log_file = tmp_path / "DATA" / "LOGS_SOUVERAINS" / "session_log.txt"
    assert expected_log_file.exists()

    with open(expected_log_file, "r") as f:
        content = f.read()
    assert "Test Message 1" in content
