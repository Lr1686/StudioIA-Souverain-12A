import log_event

def test_enregistrer_evenement_valid(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement("Test message")
    assert result is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test message" in captured.out

    assert test_log.exists()
    content = test_log.read_text()
    assert "] Test message\n" in content

def test_enregistrer_evenement_log_injection_sanitization(tmp_path, monkeypatch):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Test carriage return and newline injection attempt
    malicious_input = "User login successful\n[2026-01-01 00:00:00] Admin access granted"
    result = log_event.enregistrer_evenement(malicious_input)
    assert result is True

    lines = test_log.read_text().splitlines()
    # Ensure all content remains on a single line entry (no log forging across lines)
    assert len(lines) == 1
    assert "User login successful [2026-01-01 00:00:00] Admin access granted" in lines[0]

def test_enregistrer_evenement_invalid_inputs(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Empty string
    assert log_event.enregistrer_evenement("   ") is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message ne peut pas être vide." in captured.out

    # Non-string input
    assert log_event.enregistrer_evenement(12345) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out
