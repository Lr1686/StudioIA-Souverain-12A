import log_event


def test_enregistrer_evenement_success(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    res = log_event.enregistrer_evenement("Événement de test")
    assert res is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Événement de test" in captured.out

    assert test_log.exists()
    content = test_log.read_text(encoding="utf-8")
    assert "] Événement de test\n" in content


def test_enregistrer_evenement_log_injection(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Multiline input attempting log forgery (CWE-117)
    malicious_input = "Normal message\n[2026-01-01 00:00:00] Injected fake log entry"
    res = log_event.enregistrer_evenement(malicious_input)
    assert res is True

    content = test_log.read_text(encoding="utf-8")
    lines = content.strip().split("\n")
    # Must be logged as a single line, preventing newline-based log entry injection
    assert len(lines) == 1
    assert "Injected fake log entry" in lines[0]


def test_enregistrer_evenement_invalid_input(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Empty string or whitespace
    res = log_event.enregistrer_evenement("   \n\r  ")
    assert res is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message ne peut pas être vide." in captured.out

    # Non-string type
    res = log_event.enregistrer_evenement(12345)
    assert res is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out
