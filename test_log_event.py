import os
import log_event

def test_enregistrer_evenement_succes(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement("Test Event Normal")
    assert result is True
    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test Event Normal" in captured.out

    assert test_log.exists()
    content = test_log.read_text()
    assert "Test Event Normal" in content

def test_enregistrer_evenement_prevent_log_injection(tmp_path, monkeypatch):
    test_log = tmp_path / "LOGS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Message containing CRLF / newlines attempting log forgery
    malicious_msg = "User logged in\n[2026-01-01 00:00:00] Admin access granted"
    result = log_event.enregistrer_evenement(malicious_msg)
    assert result is True

    content = test_log.read_text()
    lines = [line for line in content.splitlines() if line]
    # Verify that only a single log entry line was written
    assert len(lines) == 1
    assert "\n" not in lines[0]
    assert "User logged in [2026-01-01 00:00:00] Admin access granted" in lines[0]

def test_enregistrer_evenement_invalid_inputs(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Non-string input
    assert log_event.enregistrer_evenement(12345) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out

    # Empty string input
    assert log_event.enregistrer_evenement("   ") is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message de log ne peut pas être vide." in captured.out
