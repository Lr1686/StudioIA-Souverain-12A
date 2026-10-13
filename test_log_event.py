import log_event

def test_enregistrer_evenement_succes(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement("Test event log")
    assert result is True
    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test event log" in captured.out

    assert test_log.exists()
    content = test_log.read_text()
    assert "] Test event log\n" in content

def test_enregistrer_evenement_input_validation(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Non-string
    assert log_event.enregistrer_evenement(12345) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out

    # Empty string
    assert log_event.enregistrer_evenement("   ") is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message ne peut pas être vide." in captured.out

    # Exceeding length limit
    long_msg = "A" * (log_event.MAX_LOG_LENGTH + 1)
    assert log_event.enregistrer_evenement(long_msg) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message dépasse la longueur maximale" in captured.out

    # Log injection with newline / control chars
    injection_msg = "Event 1\n[2026-01-01 00:00:00] Fake admin event"
    assert log_event.enregistrer_evenement(injection_msg) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message contient des caractères non autorisés" in captured.out
