import log_event

def test_enregistrer_evenement_succes(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    res = log_event.enregistrer_evenement("Événement de test réussi")
    assert res is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Événement de test réussi" in captured.out

    with open(test_log, "r") as f:
        lines = f.readlines()
    assert len(lines) == 1
    assert "Événement de test réussi" in lines[0]

def test_enregistrer_evenement_crlf_injection(tmp_path, monkeypatch):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Injection with newlines and carriage returns
    res = log_event.enregistrer_evenement("Message1\n[2026-01-01 00:00:00] Fake Log Entry\rMessage2")
    assert res is True

    with open(test_log, "r") as f:
        lines = f.readlines()
    # Should stay as a single log line (1 newline at the end)
    assert len(lines) == 1
    assert "Fake Log Entry" in lines[0]
    assert "\n[2026" not in lines[0]

def test_enregistrer_evenement_invalid_inputs(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Non-string input
    assert log_event.enregistrer_evenement(12345) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR LOG : Le message doit être une chaîne de caractères." in captured.out

    # Empty / whitespace / control char only input
    assert log_event.enregistrer_evenement("   \n\r  ") is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR LOG : Le message est vide ou invalide." in captured.out

def test_enregistrer_evenement_truncation(tmp_path, monkeypatch):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    long_msg = "A" * 600
    res = log_event.enregistrer_evenement(long_msg)
    assert res is True

    with open(test_log, "r") as f:
        content = f.read()
    assert "... [TRONQUÉ]" in content
