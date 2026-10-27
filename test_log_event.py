import log_event

def test_enregistrer_evenement_success(tmp_path, monkeypatch, capsys):
    test_log_file = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log_file))

    res = log_event.enregistrer_evenement("Test message log")
    assert res is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test message log" in captured.out

    assert test_log_file.exists()
    content = test_log_file.read_text()
    assert "] Test message log\n" in content

def test_enregistrer_evenement_invalid_input(tmp_path, monkeypatch, capsys):
    test_log_file = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log_file))

    # Empty / whitespace message
    res = log_event.enregistrer_evenement("   ")
    assert res is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message de log ne peut pas être vide." in captured.out

    # Non-string input
    res = log_event.enregistrer_evenement(12345)
    assert res is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message de log doit être une chaîne de caractères." in captured.out

    # Log injection attempt with newline / control chars
    res = log_event.enregistrer_evenement("Fake Log\n[2026-01-01 00:00:00] Injected entry")
    assert res is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message contient des caractères non autorisés" in captured.out

    # Verify log file was not created
    assert not test_log_file.exists()
