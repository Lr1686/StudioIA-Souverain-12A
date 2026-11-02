import log_event


def test_enregistrer_evenement_valid(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "SUBDIR" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement("Éveil de l'Alliée réussi")
    assert result is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Éveil de l'Alliée réussi" in captured.out

    assert test_log.exists()
    content = test_log.read_text(encoding="utf-8")
    assert content.endswith("] Éveil de l'Alliée réussi\n")


def test_enregistrer_evenement_rejects_crlf(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Reject newline injection
    result = log_event.enregistrer_evenement("Normal event\n[2026-04-13 12:00:00] Forged event")
    assert result is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message contient des caractères non autorisés." in captured.out

    # Reject carriage return
    result_cr = log_event.enregistrer_evenement("Normal event\rForged line")
    assert result_cr is False

    assert not test_log.exists()


def test_enregistrer_evenement_invalid_type_or_empty(tmp_path, monkeypatch, capsys):
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

    assert not test_log.exists()


def test_enregistrer_evenement_max_length(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    long_message = "A" * (log_event.MAX_LOG_LENGTH + 1)
    assert log_event.enregistrer_evenement(long_message) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message dépasse la longueur maximale autorisée" in captured.out

    assert not test_log.exists()
