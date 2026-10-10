import log_event

def test_enregistrer_evenement(tmp_path, monkeypatch, capsys):
    test_log_path = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log_path))

    log_event.enregistrer_evenement("Test message")
    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test message" in captured.out

    assert test_log_path.exists()
    content = test_log_path.read_text()
    assert "Test message\n" in content
