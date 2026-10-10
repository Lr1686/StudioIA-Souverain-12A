import log_event

def test_enregistrer_evenement(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Test basic message logging
    log_event.enregistrer_evenement("Test message")
    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test message" in captured.out

    assert test_log.exists()
    content = test_log.read_text()
    assert "] Test message\n" in content

def test_enregistrer_evenement_log_injection(tmp_path, monkeypatch):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Test log injection prevention with embedded newlines
    malicious_message = "Normal event\n[2026-01-01 00:00:00] Fake admin event"
    log_event.enregistrer_evenement(malicious_message)

    content = test_log.read_text()
    lines = [line for line in content.splitlines() if line.strip()]

    # Should be exactly 1 log entry line, not split into 2 separate lines
    assert len(lines) == 1
    assert "Normal event\\n[2026-01-01 00:00:00] Fake admin event" in lines[0]
