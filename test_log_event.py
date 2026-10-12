import log_event

def test_enregistrer_evenement(tmp_path, monkeypatch, capsys):
    test_log_file = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log_file))

    log_event.enregistrer_evenement("Test audit log event")

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test audit log event" in captured.out
    assert test_log_file.exists()

    content = test_log_file.read_text()
    assert "Test audit log event" in content
