import log_event

def test_enregistrer_evenement_success(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    res = log_event.enregistrer_evenement("Test valid message")
    assert res is True
    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test valid message" in captured.out

    with open(test_log, "r") as f:
        content = f.read()
    assert "Test valid message" in content

def test_enregistrer_evenement_invalid_inputs(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Non-string input
    res = log_event.enregistrer_evenement(12345)
    assert res is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out

    # Empty string
    res = log_event.enregistrer_evenement("   ")
    assert res is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message d'événement ne peut pas être vide." in captured.out

    # Overly long string (> 500 chars)
    res = log_event.enregistrer_evenement("A" * 501)
    assert res is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message dépasse la longueur maximale autorisée" in captured.out

    # Control character / Newline (Log Injection attempt)
    res = log_event.enregistrer_evenement("Fake Log\n[2026-01-01 00:00:00] Admin access granted")
    assert res is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message contient des caractères non autorisés." in captured.out
