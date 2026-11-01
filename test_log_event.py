import log_event


def test_enregistrer_evenement_valid(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "logs" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement("Test event log message")
    assert result is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test event log message" in captured.out

    assert test_log.exists()
    content = test_log.read_text()
    assert "Test event log message\n" in content
    assert content.startswith("[")


def test_enregistrer_evenement_rejects_log_injection(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Reject newlines / carriage returns to prevent fake log forging
    bad_messages = [
        "Normal message\n[2026-04-13 12:00:00] Injected fake log entry",
        "Fake\r\nLog injection",
        "Tab or control \x00 character",
    ]

    for bad_msg in bad_messages:
        result = log_event.enregistrer_evenement(bad_msg)
        assert result is False
        captured = capsys.readouterr()
        assert "⚠️ ERREUR : Le message contient des caractères non autorisés" in captured.out

    assert not test_log.exists()


def test_enregistrer_evenement_input_validation(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Non-string
    assert log_event.enregistrer_evenement(12345) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out

    # Empty / whitespace-only
    assert log_event.enregistrer_evenement("   ") is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message ne peut pas être vide." in captured.out

    # Exceeding MAX_MESSAGE_LENGTH
    assert log_event.enregistrer_evenement("A" * 501) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message dépasse la longueur maximale autorisée" in captured.out
