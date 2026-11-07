import log_event


def test_enregistrer_evenement_success(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    res = log_event.enregistrer_evenement("Test message normal")
    assert res is True
    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test message normal" in captured.out

    lines = test_log.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    assert lines[0].endswith("] Test message normal")


def test_enregistrer_evenement_crlf_sanitization(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Attempt log injection with CRLF
    injected_message = (
        "Normal event\n[2026-01-01 00:00:00] Injected fake event\r\nAnother forged line"
    )
    res = log_event.enregistrer_evenement(injected_message)
    assert res is True

    lines = test_log.read_text(encoding="utf-8").splitlines()
    # Log entry must be sanitized into a single line to prevent log forging
    assert len(lines) == 1
    assert "Injected fake event" in lines[0]
    assert "\n" not in lines[0]
    assert "\r" not in lines[0]


def test_enregistrer_evenement_invalid_inputs(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Empty string
    assert log_event.enregistrer_evenement("   ") is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message ne peut pas être vide." in captured.out

    # Non-string
    assert log_event.enregistrer_evenement(12345) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out

    # Oversized input
    assert log_event.enregistrer_evenement("A" * 501) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message dépasse la longueur maximale" in captured.out

    # Verify nothing was written to test_log
    assert not test_log.exists()
