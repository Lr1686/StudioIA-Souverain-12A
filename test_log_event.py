import log_event

def test_enregistrer_evenement(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Test registering event when directory does not exist yet
    log_event.enregistrer_evenement("Test message 1")
    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test message 1" in captured.out

    assert test_log.exists()
    content = test_log.read_text()
    assert "Test message 1" in content

    # Test registering second event when directory already exists
    log_event.enregistrer_evenement("Test message 2")
    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test message 2" in captured.out

    lines = test_log.read_text().strip().split("\n")
    assert len(lines) == 2
    assert "Test message 1" in lines[0]
    assert "Test message 2" in lines[1]
