import log_event


def test_enregistrer_evenement_success(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement("Éveil du système")
    assert result is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Éveil du système" in captured.out

    assert test_log.exists()
    content = test_log.read_text(encoding="utf-8")
    assert "Éveil du système" in content
    assert content.endswith("\n")


def test_enregistrer_evenement_rejects_newlines_log_injection(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Log injection attempt with newline
    result = log_event.enregistrer_evenement("Normal event\n[2026-01-01 00:00:00] Admin access granted")
    assert result is False

    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message contient des caractères non autorisés." in captured.out
    assert not test_log.exists()


def test_enregistrer_evenement_rejects_carriage_return(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement("First line\rSecond line")
    assert result is False

    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message contient des caractères non autorisés." in captured.out
    assert not test_log.exists()


def test_enregistrer_evenement_empty_or_whitespace(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement("   ")
    assert result is False

    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message ne peut pas être vide." in captured.out
    assert not test_log.exists()


def test_enregistrer_evenement_non_string(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement(12345)
    assert result is False

    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out
    assert not test_log.exists()


def test_enregistrer_evenement_max_length_exceeded(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement("A" * 501)
    assert result is False

    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message dépasse la longueur maximale autorisée" in captured.out
    assert not test_log.exists()
