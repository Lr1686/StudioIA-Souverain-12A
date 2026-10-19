import log_event

def test_enregistrer_evenement_success(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement("Test event message")
    assert result is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test event message" in captured.out

    assert test_log.exists()
    content = test_log.read_text()
    assert "] Test event message\n" in content

def test_enregistrer_evenement_invalid_inputs(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Non-string input
    assert log_event.enregistrer_evenement(12345) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message de log doit être une chaîne de caractères." in captured.out

    # Empty string input
    assert log_event.enregistrer_evenement("   ") is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message de log ne peut pas être vide." in captured.out

    # Oversized input
    assert log_event.enregistrer_evenement("A" * 501) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message de log dépasse la longueur maximale" in captured.out

    # Newline / log injection attempt
    assert log_event.enregistrer_evenement("Fake Log\n[2026-01-01 00:00:00] Injected Log Entry") is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message de log contient des caractères non autorisés" in captured.out

    # Confirm log file was not created for invalid inputs
    assert not test_log.exists()
