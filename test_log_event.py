import log_event


def test_enregistrer_evenement_success(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    success = log_event.enregistrer_evenement("Test sovereign event")
    assert success is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test sovereign event" in captured.out

    with open(test_log, "r") as f:
        content = f.read()

    assert "Test sovereign event" in content
    assert content.endswith("Test sovereign event\n")


def test_enregistrer_evenement_creates_missing_directory(tmp_path, monkeypatch):
    nested_log = tmp_path / "subdir" / "logs" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(nested_log))

    success = log_event.enregistrer_evenement("Directory created")
    assert success is True
    assert nested_log.exists()


def test_enregistrer_evenement_log_injection_prevention(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Reject newline injection
    newline_injection = "Normal event\n[2026-04-13 12:00:00] Injected fake log entry"
    success = log_event.enregistrer_evenement(newline_injection)
    assert success is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message contient des caractères de contrôle ou retours à la ligne non autorisés." in captured.out
    assert not test_log.exists()

    # Reject carriage return injection
    cr_injection = "Normal event\r[2026-04-13 12:00:00] Injected fake log entry"
    success = log_event.enregistrer_evenement(cr_injection)
    assert success is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message contient des caractères de contrôle ou retours à la ligne non autorisés." in captured.out
    assert not test_log.exists()


def test_enregistrer_evenement_input_validation(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Non-string input
    assert log_event.enregistrer_evenement(12345) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out

    # Empty message
    assert log_event.enregistrer_evenement("   ") is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message d'événement ne peut pas être vide." in captured.out

    # Message exceeding MAX_MESSAGE_LENGTH
    long_msg = "A" * (log_event.MAX_MESSAGE_LENGTH + 1)
    assert log_event.enregistrer_evenement(long_msg) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message dépasse la longueur maximale autorisée" in captured.out

    assert not test_log.exists()
