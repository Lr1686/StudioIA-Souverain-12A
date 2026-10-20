import log_event

def test_enregistrer_evenement_normal(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    log_event.enregistrer_evenement("Test normal event")
    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test normal event" in captured.out

    assert test_log.exists()
    content = test_log.read_text()
    assert "Test normal event" in content

def test_enregistrer_evenement_log_injection_sanitization(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    malicious_msg = "User action\n[2026-01-01 00:00:00] [CRITICAL] Admin privileges granted to attacker"
    log_event.enregistrer_evenement(malicious_msg)

    assert test_log.exists()
    lines = test_log.read_text().strip().split("\n")
    # Verify that the newline was replaced and the entire entry is recorded on a single log line
    assert len(lines) == 1
    assert "Admin privileges granted" in lines[0]
