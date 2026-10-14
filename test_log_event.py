import os
import log_event

def test_enregistrer_evenement_normal(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement("Événement de test")
    assert result is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Événement de test" in captured.out

    assert os.path.exists(test_log)
    with open(test_log, "r") as f:
        lines = f.readlines()
    assert len(lines) == 1
    assert "Événement de test" in lines[0]

def test_enregistrer_evenement_log_injection(tmp_path, monkeypatch):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Input containing newlines and control characters attempting log forging
    malicious_input = "System Boot\n[2026-01-01 00:00:00] Admin access granted"
    result = log_event.enregistrer_evenement(malicious_input)
    assert result is True

    with open(test_log, "r") as f:
        lines = f.readlines()
    # Must only produce 1 line in the log file
    assert len(lines) == 1
    assert "\n" not in lines[0][:-1]  # No unexpected embedded newlines

def test_enregistrer_evenement_invalid_input(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Empty / whitespace message
    res_empty = log_event.enregistrer_evenement("   ")
    assert res_empty is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message ne peut pas être vide." in captured.out

    # Non-string input
    res_num = log_event.enregistrer_evenement(12345)
    assert res_num is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out

def test_enregistrer_evenement_length_limit(tmp_path, monkeypatch):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    long_message = "A" * 600
    res = log_event.enregistrer_evenement(long_message)
    assert res is True

    with open(test_log, "r") as f:
        content = f.read()
    # Message portion should be truncated to MAX_LOG_LENGTH (500 chars)
    assert "A" * 500 in content
    assert "A" * 501 not in content
