import log_event

def test_enregistrer_evenement(tmp_path, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    log_event.enregistrer_evenement("Test message", log_path=str(test_log))

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test message" in captured.out

    assert test_log.exists()
    content = test_log.read_text()
    assert "Test message" in content
