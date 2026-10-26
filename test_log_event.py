import log_event


def test_enregistrer_evenement_normal(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    log_event.enregistrer_evenement("Événement de test")
    captured = capsys.readouterr()

    assert "🔱 ÉVÉNEMENT GRAVÉ : Événement de test" in captured.out
    assert test_log.exists()

    content = test_log.read_text()
    assert "Événement de test" in content
    assert content.count("\n") == 1


def test_enregistrer_evenement_log_injection_sanitization(tmp_path, monkeypatch):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Attempt log injection with newline and fake timestamp/event
    malicious_msg = "Event 1\n[2026-01-01 00:00:00] FAKE EVENT: Admin bypass"
    log_event.enregistrer_evenement(malicious_msg)

    content = test_log.read_text()
    # Ensure there is exactly one log line in the file (no injected newlines)
    lines = [line for line in content.split("\n") if line]
    assert len(lines) == 1
    assert "FAKE EVENT: Admin bypass" in lines[0]


def test_enregistrer_evenement_non_string_input(tmp_path, monkeypatch):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    log_event.enregistrer_evenement(12345)
    content = test_log.read_text()
    assert "12345" in content


def test_enregistrer_evenement_empty_input(tmp_path, monkeypatch):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    log_event.enregistrer_evenement("   \n\t  ")
    content = test_log.read_text()
    assert "[EMPTY_MESSAGE]" in content
