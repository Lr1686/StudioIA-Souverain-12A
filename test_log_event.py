import log_event


def test_enregistrer_evenement_success(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement("Événement valide")
    assert result is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Événement valide" in captured.out

    with open(test_log, "r") as f:
        content = f.read()
    assert "] Événement valide\n" in content


def test_enregistrer_evenement_invalid_type(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement(12345)
    assert result is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out
    assert not test_log.exists()


def test_enregistrer_evenement_empty(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement("   \t  ")
    assert result is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message de log ne peut pas être vide." in captured.out
    assert not test_log.exists()


def test_enregistrer_evenement_log_injection_newlines(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Attempt log injection using newline
    injection = "Normal log\n[2026-04-13 18:27:57] FORGED SOVEREIGN EVENT"
    result = log_event.enregistrer_evenement(injection)
    assert result is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message contient des caractères non autorisés" in captured.out
    assert not test_log.exists()


def test_enregistrer_evenement_max_length(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    oversized = "A" * (log_event.MAX_MESSAGE_LENGTH + 1)
    result = log_event.enregistrer_evenement(oversized)
    assert result is False
    captured = capsys.readouterr()
    assert (
        "⚠️ ERREUR : Le message dépasse la longueur maximale autorisée" in captured.out
    )
    assert not test_log.exists()
