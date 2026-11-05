import log_event


def test_enregistrer_evenement_success(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement("Test message log")
    assert result is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test message log" in captured.out

    assert test_log.exists()
    content = test_log.read_text(encoding="utf-8")
    assert "Test message log" in content
    assert content.endswith("\n")


def test_enregistrer_evenement_rejects_crlf_log_injection(
    tmp_path, monkeypatch, capsys
):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Attempt Log Injection / CRLF injection
    malicious_msg = "Normal message\n[2026-01-01 00:00:00] Injected fake log entry"
    result = log_event.enregistrer_evenement(malicious_msg)
    assert result is False

    captured = capsys.readouterr()
    assert (
        "⚠️ ERREUR : Le message contient des caractères non autorisés." in captured.out
    )
    assert not test_log.exists()


def test_enregistrer_evenement_rejects_carriage_return(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement("Message\rInjected line")
    assert result is False

    captured = capsys.readouterr()
    assert (
        "⚠️ ERREUR : Le message contient des caractères non autorisés." in captured.out
    )
    assert not test_log.exists()


def test_enregistrer_evenement_rejects_empty():
    result = log_event.enregistrer_evenement("   ")
    assert result is False


def test_enregistrer_evenement_rejects_oversized_input(capsys):
    long_msg = "X" * (log_event.MAX_LOG_LENGTH + 1)
    result = log_event.enregistrer_evenement(long_msg)
    assert result is False

    captured = capsys.readouterr()
    assert (
        "⚠️ ERREUR : Le message dépasse la longueur maximale autorisée" in captured.out
    )


def test_enregistrer_evenement_rejects_invalid_type(capsys):
    result = log_event.enregistrer_evenement(12345)
    assert result is False

    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out
