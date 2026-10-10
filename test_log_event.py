import log_event

def test_enregistrer_evenement_normal(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    res = log_event.enregistrer_evenement("Événement de test")
    assert res is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Événement de test" in captured.out

    assert test_log.exists()
    content = test_log.read_text()
    assert "Événement de test" in content
    assert "\n" in content


def test_enregistrer_evenement_log_injection_sanitization(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Message containing newline log injection attempt
    injection_msg = "User logged in\n[2026-01-01 00:00:00] [ADMIN] Granted root access"
    res = log_event.enregistrer_evenement(injection_msg)
    assert res is True

    content = test_log.read_text()
    # Ensure there is only 1 entry line (newline was neutralized into space)
    lines = [line for line in content.splitlines() if line.strip()]
    assert len(lines) == 1
    assert "Granted root access" in lines[0]


def test_enregistrer_evenement_invalid_and_empty_inputs(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Non-string input
    assert log_event.enregistrer_evenement(12345) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out

    # Empty / whitespace-only string
    assert log_event.enregistrer_evenement("   \n\r  ") is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message de log ne peut pas être vide." in captured.out
