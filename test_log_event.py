import log_event

def test_enregistrer_evenement_success(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "test_session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    success = log_event.enregistrer_evenement("Système initialisé avec succès")
    assert success is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Système initialisé avec succès" in captured.out

    assert test_log.exists()
    content = test_log.read_text()
    assert "Système initialisé avec succès\n" in content
    assert content.startswith("[")

def test_enregistrer_evenement_prevents_newline_log_injection(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "test_session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Attempt log forging injection via carriage return / newline
    result = log_event.enregistrer_evenement("Fake Entry\n[2026-01-01 00:00:00] Injected fake log")
    assert result is False

    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message contient des caractères de contrôle non autorisés." in captured.out
    assert not test_log.exists()

def test_enregistrer_evenement_invalid_input(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "test_session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Empty string
    assert log_event.enregistrer_evenement("   ") is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message de log ne peut pas être vide." in captured.out

    # Non-string input
    assert log_event.enregistrer_evenement({"event": "bad"}) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out

    # Message exceeds max length
    assert log_event.enregistrer_evenement("X" * (log_event.MAX_LOG_MESSAGE_LENGTH + 1)) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message dépasse la longueur maximale autorisée" in captured.out
