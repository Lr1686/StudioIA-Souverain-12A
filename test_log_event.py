import os
import log_event

def test_enregistrer_evenement_success(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    res = log_event.enregistrer_evenement("Test message")
    assert res is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test message" in captured.out

    with open(test_log, "r") as f:
        content = f.read()
    assert "Test message" in content

def test_enregistrer_evenement_invalid_inputs(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Non-string input
    res = log_event.enregistrer_evenement(12345)
    assert res is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out

    # Empty / whitespace-only string
    res = log_event.enregistrer_evenement("   \n  ")
    assert res is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message ne peut pas être vide." in captured.out

def test_enregistrer_evenement_log_injection(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Message containing newline characters trying to inject fake log entry
    malicious_msg = "Normal event\n[2026-01-01 00:00:00] [FAKE_ADMIN] Unauthorized action executed"
    res = log_event.enregistrer_evenement(malicious_msg)
    assert res is True

    with open(test_log, "r") as f:
        lines = f.readlines()

    # Verify log entry is contained in exactly 1 line (newline sanitized)
    assert len(lines) == 1
    assert "FAKE_ADMIN" in lines[0]
    assert "\n" not in lines[0].strip()
