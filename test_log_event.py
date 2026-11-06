import log_event


def test_enregistrer_evenement_success(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement("Événement de test")
    assert result is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Événement de test" in captured.out

    with open(test_log, "r") as f:
        content = f.read()
    assert "Événement de test\n" in content


def test_enregistrer_evenement_log_injection(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Test newline injection attempt
    result = log_event.enregistrer_evenement("Normal event\n[2026-11-06 00:00:00] Forged event")
    assert result is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message contient des caractères de contrôle non autorisés." in captured.out
    assert not test_log.exists()

    # Test carriage return injection attempt
    result = log_event.enregistrer_evenement("Normal event\rForged")
    assert result is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message contient des caractères de contrôle non autorisés." in captured.out
    assert not test_log.exists()


def test_enregistrer_evenement_invalid_input(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Non-string input
    result = log_event.enregistrer_evenement(12345)
    assert result is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out

    # Empty string
    result = log_event.enregistrer_evenement("   ")
    assert result is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message ne peut pas être vide." in captured.out

    # Overly long message
    result = log_event.enregistrer_evenement("A" * 501)
    assert result is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message dépasse la longueur maximale autorisée" in captured.out
    assert not test_log.exists()
