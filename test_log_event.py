import log_event


def test_enregistrer_evenement_success(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement("Test audit message")
    assert result is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test audit message" in captured.out

    assert test_log.exists()
    content = test_log.read_text(encoding="utf-8")
    assert content.endswith("] Test audit message\n")


def test_enregistrer_evenement_rejects_non_string(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    assert log_event.enregistrer_evenement(12345) is False
    assert not test_log.exists()

    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out


def test_enregistrer_evenement_rejects_empty(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    assert log_event.enregistrer_evenement("   ") is False
    assert not test_log.exists()

    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message ne peut pas être vide." in captured.out


def test_enregistrer_evenement_rejects_too_long(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    long_message = "A" * 501
    assert log_event.enregistrer_evenement(long_message) is False
    assert not test_log.exists()

    captured = capsys.readouterr()
    assert (
        "⚠️ ERREUR : Le message dépasse la longueur maximale autorisée" in captured.out
    )


def test_enregistrer_evenement_prevents_log_injection(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Reject newline injection
    assert (
        log_event.enregistrer_evenement(
            "Valid msg\n[2026-01-01 00:00:00] Forged log entry"
        )
        is False
    )
    # Reject carriage return injection
    assert (
        log_event.enregistrer_evenement(
            "Valid msg\r[2026-01-01 00:00:00] Forged log entry"
        )
        is False
    )
    # Reject other control characters
    assert log_event.enregistrer_evenement("Valid msg\x00corrupt") is False
    assert not test_log.exists()

    captured = capsys.readouterr()
    assert (
        "⚠️ ERREUR : Le message contient des caractères non autorisés." in captured.out
    )
