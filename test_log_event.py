import log_event


def test_enregistrer_evenement_success(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    res = log_event.enregistrer_evenement("Éveil du système validé")
    assert res is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Éveil du système validé" in captured.out

    assert test_log.exists()
    content = test_log.read_text(encoding="utf-8")
    assert content.endswith("Éveil du système validé\n")
    assert content.startswith("[")


def test_enregistrer_evenement_invalid_input(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Non-string input
    res = log_event.enregistrer_evenement(12345)
    assert res is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out

    # Empty string or whitespace
    res = log_event.enregistrer_evenement("   ")
    assert res is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message ne peut pas être vide." in captured.out

    # Overly long message (>500 chars)
    res = log_event.enregistrer_evenement("A" * 501)
    assert res is False
    captured = capsys.readouterr()
    assert (
        "⚠️ ERREUR : Le message dépasse la longueur maximale autorisée" in captured.out
    )

    # Log injection attempt with newline
    res = log_event.enregistrer_evenement(
        "Faux message\n[2026-01-01 00:00:00] Injected fake log entry"
    )
    assert res is False
    captured = capsys.readouterr()
    assert (
        "⚠️ ERREUR : Le message contient des caractères non autorisés." in captured.out
    )

    # Control character
    res = log_event.enregistrer_evenement("Message with \x00 null byte")
    assert res is False
    captured = capsys.readouterr()
    assert (
        "⚠️ ERREUR : Le message contient des caractères non autorisés." in captured.out
    )

    # Ensure log file was never created
    assert not test_log.exists()
