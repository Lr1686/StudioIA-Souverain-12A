import log_event


def test_enregistrer_evenement_valid(tmp_path, monkeypatch, capsys):
    log_file = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(log_file))

    res = log_event.enregistrer_evenement("Test event message")
    assert res is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test event message" in captured.out

    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    lines = content.strip().splitlines()
    assert len(lines) == 1
    assert "Test event message" in lines[0]


def test_enregistrer_evenement_invalid_type(tmp_path, monkeypatch, capsys):
    log_file = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(log_file))

    res = log_event.enregistrer_evenement(12345)
    assert res is False

    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message de log doit être une chaîne de caractères." in captured.out
    assert not log_file.exists()


def test_enregistrer_evenement_log_injection(tmp_path, monkeypatch, capsys):
    log_file = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(log_file))

    injection_payload = "User logged in\n[2026-01-01 00:00:00] [CRITICAL] Admin privileges granted\rFake line"
    res = log_event.enregistrer_evenement(injection_payload)
    assert res is True

    content = log_file.read_text(encoding="utf-8")
    lines = content.strip().splitlines()
    # Ensure log payload was sanitized so it stays strictly on 1 single line
    assert len(lines) == 1
    assert "\\n[2026-01-01 00:00:00] [CRITICAL] Admin privileges granted\\rFake line" in lines[0]
