import log_event

def test_enregistrer_evenement_valid(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    res = log_event.enregistrer_evenement("Test normal message")
    assert res is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test normal message" in captured.out

    lines = test_log.read_text().splitlines()
    assert len(lines) == 1
    assert "Test normal message" in lines[0]

def test_enregistrer_evenement_crlf_injection(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Attempt log injection with newline and fake timestamp
    malicious_msg = "User logged in\n[2026-01-01 00:00:00] [CRITICAL] Admin rights granted to attacker"
    res = log_event.enregistrer_evenement(malicious_msg)
    assert res is True

    lines = test_log.read_text().splitlines()
    # Must remain a single log line, preventing line injection
    assert len(lines) == 1
    assert "\n" not in lines[0]
    assert "User logged in [2026-01-01 00:00:00] [CRITICAL] Admin rights granted to attacker" in lines[0]

def test_enregistrer_evenement_invalid_inputs(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Non-string input
    assert log_event.enregistrer_evenement(12345) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message de log doit être une chaîne de caractères." in captured.out

    # Empty string input
    assert log_event.enregistrer_evenement("   ") is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message de log ne peut pas être vide." in captured.out
