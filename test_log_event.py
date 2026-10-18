import log_event


def test_enregistrer_evenement_succes(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    res = log_event.enregistrer_evenement("Événement de test réussi")
    assert res is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Événement de test réussi" in captured.out

    assert test_log.exists()
    content = test_log.read_text()
    assert "Événement de test réussi" in content


def test_enregistrer_evenement_invalide(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Type invalide
    assert log_event.enregistrer_evenement(12345) is False
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in capsys.readouterr().out

    # Message vide
    assert log_event.enregistrer_evenement("   ") is False
    assert "⚠️ ERREUR : Le message ne peut pas être vide." in capsys.readouterr().out

    # Message trop long
    assert log_event.enregistrer_evenement("A" * 501) is False
    assert "⚠️ ERREUR : Le message dépasse la longueur maximale" in capsys.readouterr().out

    # Injection de saut de ligne / caractères de contrôle
    assert log_event.enregistrer_evenement("Message\nFaux_Log_Injecte") is False
    assert "⚠️ ERREUR : Le message contient des caractères non autorisés" in capsys.readouterr().out
