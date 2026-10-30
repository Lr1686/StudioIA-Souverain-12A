import log_event

def test_enregistrer_evenement(tmp_path, monkeypatch, capsys):
    log_file = tmp_path / "DATA" / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(log_file))

    res = log_event.enregistrer_evenement("Test normal event")
    assert res is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test normal event" in captured.out

    assert log_file.exists()
    content = log_file.read_text()
    assert "Test normal event" in content
    # Verify line count is 1
    lines = [line for line in content.splitlines() if line.strip()]
    assert len(lines) == 1

def test_enregistrer_evenement_crlf_injection(tmp_path, monkeypatch, capsys):
    log_file = tmp_path / "DATA" / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(log_file))

    injected_message = "Normal log\n[2026-01-01 00:00:00] FAKE INJECTED LOG ENTRY"
    res = log_event.enregistrer_evenement(injected_message)
    assert res is True

    captured = capsys.readouterr()
    assert "Normal log\\n[2026-01-01 00:00:00] FAKE INJECTED LOG ENTRY" in captured.out

    content = log_file.read_text()
    lines = [line for line in content.splitlines() if line.strip()]
    # CRITICAL: It must remain exactly ONE log line, preventing injection of a fake line
    assert len(lines) == 1
    assert "Normal log\\n[2026-01-01 00:00:00] FAKE INJECTED LOG ENTRY" in lines[0]

def test_enregistrer_evenement_invalid_input(tmp_path, monkeypatch, capsys):
    log_file = tmp_path / "DATA" / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(log_file))

    res = log_event.enregistrer_evenement(12345)
    assert res is False

    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message d'événement doit être une chaîne de caractères." in captured.out
    assert not log_file.exists()
