import log_event

def test_enregistrer_evenement_valid(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    res = log_event.enregistrer_evenement("Test normal message")
    assert res is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test normal message" in captured.out

    lines = test_log.read_text().strip().splitlines()
    assert len(lines) == 1
    assert "Test normal message" in lines[0]

def test_enregistrer_evenement_log_injection_prevention(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    malicious_input = "System OK\n[2026-01-01 00:00:00] [CRITICAL] Admin privilège accordé!"
    res = log_event.enregistrer_evenement(malicious_input)
    assert res is True

    captured = capsys.readouterr()
    # Newlines should be converted to single spaces
    assert "System OK [2026-01-01 00:00:00] [CRITICAL] Admin privilège accordé!" in captured.out

    lines = test_log.read_text().strip().splitlines()
    # Must only be 1 line, log entry forging failed!
    assert len(lines) == 1
    assert "\n" not in lines[0]

def test_enregistrer_evenement_invalid_input(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Non-string input
    res = log_event.enregistrer_evenement(12345)
    assert res is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out

    # Empty string / whitespace
    res = log_event.enregistrer_evenement("   \n   ")
    assert res is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message ne peut pas être vide." in captured.out
