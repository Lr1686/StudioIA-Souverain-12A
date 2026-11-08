import log_event


def test_enregistrer_evenement_success(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "logs" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement("Test message souverain")
    assert result is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test message souverain" in captured.out

    assert test_log.exists()
    content = test_log.read_text()
    assert "Test message souverain\n" in content
    assert content.startswith("[")


def test_enregistrer_evenement_invalid_inputs(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "logs" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Non-string input
    assert log_event.enregistrer_evenement(12345) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out

    # Empty string or whitespace only
    assert log_event.enregistrer_evenement("   ") is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message ne peut pas être vide." in captured.out

    # Exceeding MAX_LOG_LENGTH (500)
    assert log_event.enregistrer_evenement("X" * 501) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message dépasse la longueur maximale autorisée" in captured.out


def test_enregistrer_evenement_prevents_log_injection(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "logs" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Newline injection attempt
    injection_newline = "Valid message\n[2026-04-13 12:00:00] Injected fake event"
    assert log_event.enregistrer_evenement(injection_newline) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message contient des caractères non autorisés." in captured.out

    # Carriage return injection attempt
    injection_cr = "Valid message\r[2026-04-13 12:00:00] Injected fake event"
    assert log_event.enregistrer_evenement(injection_cr) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message contient des caractères non autorisés." in captured.out

    # Other control character (e.g., null byte or bell)
    injection_ctrl = "Malicious\x00message"
    assert log_event.enregistrer_evenement(injection_ctrl) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message contient des caractères non autorisés." in captured.out

    # Ensure log file was never created / modified
    assert not test_log.exists()
