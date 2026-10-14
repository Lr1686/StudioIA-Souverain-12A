import log_event

def test_enregistrer_evenement_success(tmp_path, monkeypatch, capsys):
    log_file = tmp_path / "LOGS" / "test_session.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(log_file), raising=False)

    # Patch log_path in function scope if referenced directly or update log_event module
    # Let's test standard log recording
    result = log_event.enregistrer_evenement("Test message log")
    assert result is True
    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test message log" in captured.out

def test_enregistrer_evenement_invalid_input(capsys):
    # Non-string input
    result = log_event.enregistrer_evenement(12345)
    assert result is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message de log doit être une chaîne de caractères." in captured.out

    # Empty / whitespace-only input
    result = log_event.enregistrer_evenement("   \n  ")
    assert result is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message de log ne peut pas être vide." in captured.out

def test_enregistrer_evenement_log_injection_sanitization(tmp_path, monkeypatch, capsys):
    log_file = tmp_path / "LOGS" / "test_session_injection.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(log_file))

    # Test CRLF / log injection attack payload
    injection_payload = "User login\n[2026-04-13 18:00:00] Admin login forged"
    result = log_event.enregistrer_evenement(injection_payload)
    assert result is True
    captured = capsys.readouterr()
    # Newlines should be sanitized to space
    assert "User login [2026-04-13 18:00:00] Admin login forged" in captured.out
