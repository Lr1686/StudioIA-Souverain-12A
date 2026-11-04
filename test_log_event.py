import log_event

def test_enregistrer_evenement_success(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "sub" / "test_session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement("Test sovereign event")
    assert result is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test sovereign event" in captured.out

    assert test_log.exists()
    content = test_log.read_text()
    assert "Test sovereign event\n" in content

def test_enregistrer_evenement_non_string(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "test_session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement(12345)
    assert result is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out
    assert not test_log.exists()

def test_enregistrer_evenement_empty(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "test_session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement("   \t  ")
    assert result is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message ne peut pas être vide." in captured.out
    assert not test_log.exists()

def test_enregistrer_evenement_too_long(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "test_session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    long_msg = "X" * 501
    result = log_event.enregistrer_evenement(long_msg)
    assert result is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message dépasse la longueur maximale autorisée" in captured.out
    assert not test_log.exists()

def test_enregistrer_evenement_log_injection(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "test_session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Newline character injection (CWE-117)
    forged_msg = "Event 1\n[2026-04-13 12:00:00] Forged admin event"
    result = log_event.enregistrer_evenement(forged_msg)
    assert result is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message contient des caractères de contrôle non autorisés." in captured.out
    assert not test_log.exists()

    # Carriage return injection
    forged_msg_cr = "Event 1\rForged log line"
    result = log_event.enregistrer_evenement(forged_msg_cr)
    assert result is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message contient des caractères de contrôle non autorisés." in captured.out
    assert not test_log.exists()
