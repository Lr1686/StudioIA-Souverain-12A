import log_event

def test_enregistrer_evenement_normal(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    log_event.enregistrer_evenement("Test normal event")
    captured = capsys.readouterr()

    assert "🔱 ÉVÉNEMENT GRAVÉ : Test normal event" in captured.out
    assert test_log.exists()

    with open(test_log, "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert len(lines) == 1
    assert "] Test normal event\n" in lines[0]


def test_enregistrer_evenement_log_injection_sanitization(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    malicious_input = "User action\r\n[2026-01-01 00:00:00] FORGED ADMIN LOG\nAnother forged line"
    log_event.enregistrer_evenement(malicious_input)

    with open(test_log, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Verify log injection is prevented: exactly one line written
    assert len(lines) == 1
    assert "FORGED ADMIN LOG" in lines[0]
    assert "\n" not in lines[0][:-1]  # No unexpected embedded newlines
    assert "\r" not in lines[0]


def test_enregistrer_evenement_non_string_input(tmp_path, monkeypatch):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    log_event.enregistrer_evenement(12345)

    with open(test_log, "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert len(lines) == 1
    assert "] 12345\n" in lines[0]
