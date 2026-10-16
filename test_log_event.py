import log_event

def test_enregistrer_evenement_success(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement("Test event log")
    assert result is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test event log" in captured.out

    with open(test_log, "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert len(lines) == 1
    assert "Test event log" in lines[0]

def test_enregistrer_evenement_log_injection_sanitization(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Attempt log injection with newline character
    malicious_msg = "Legit event\n[2026-01-01 00:00:00] Fake forged event"
    result = log_event.enregistrer_evenement(malicious_msg)
    assert result is True

    with open(test_log, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Must be written as a single line, with newline converted to space
    assert len(lines) == 1
    assert "\n" not in lines[0][:-1]  # No inner newline
    assert "Legit event [2026-01-01 00:00:00] Fake forged event" in lines[0]

def test_enregistrer_evenement_validation(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Non-string input
    assert log_event.enregistrer_evenement(12345) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out

    # Empty / whitespace input
    assert log_event.enregistrer_evenement("   ") is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message ne peut pas être vide." in captured.out

    # Excessively long message
    long_msg = "x" * 501
    assert log_event.enregistrer_evenement(long_msg) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message dépasse la longueur maximale autorisée" in captured.out
