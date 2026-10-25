import log_event

def test_enregistrer_evenement_validation(capsys):
    # Non-string input
    res = log_event.enregistrer_evenement(12345)
    assert res is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message de log doit être une chaîne de caractères." in captured.out

    # Empty message
    res = log_event.enregistrer_evenement("   ")
    assert res is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message de log ne peut pas être vide." in captured.out

    # Exceed max length (> 500 chars)
    res = log_event.enregistrer_evenement("A" * 501)
    assert res is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message dépasse la longueur maximale autorisée" in captured.out

    # Control characters / newline (Log Injection attempt)
    res = log_event.enregistrer_evenement("Normal event\n[2026-01-01 00:00:00] FAKE INJECTED EVENT")
    assert res is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message de log contient des caractères de contrôle non autorisés." in captured.out

def test_enregistrer_evenement_success(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    res = log_event.enregistrer_evenement("Événement de test sécurisé")
    assert res is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Événement de test sécurisé" in captured.out

    with open(test_log, "r") as f:
        content = f.read()
    assert "] Événement de test sécurisé\n" in content
