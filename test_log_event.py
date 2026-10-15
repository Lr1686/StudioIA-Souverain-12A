import log_event

def test_enregistrer_evenement_valid(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement("Événement de test")
    assert result is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Événement de test" in captured.out

    with open(test_log, "r") as f:
        lines = f.readlines()
    assert len(lines) == 1
    assert "Événement de test\n" in lines[0]

def test_enregistrer_evenement_log_injection(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Attempt log injection with embedded newlines
    malicious_msg = "User logged in\n[2026-03-30 12:00:00] [CRITICAL] Admin privilege granted"
    result = log_event.enregistrer_evenement(malicious_msg)
    assert result is True

    with open(test_log, "r") as f:
        lines = f.readlines()
    # Ensure it stays on a single line instead of creating multiple log entries
    assert len(lines) == 1
    assert "\n" not in lines[0][:-1]  # No inner newlines
    assert "User logged in [2026-03-30 12:00:00] [CRITICAL] Admin privilege granted" in lines[0]

def test_enregistrer_evenement_invalid_inputs(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Non-string input
    assert log_event.enregistrer_evenement(12345) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message de log doit être une chaîne de caractères." in captured.out

    # Empty / whitespace-only input
    assert log_event.enregistrer_evenement("   \n\r  ") is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message de log ne peut pas être vide." in captured.out
