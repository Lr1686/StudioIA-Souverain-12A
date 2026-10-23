import os
import log_event

def test_enregistrer_evenement_success(tmp_path, monkeypatch, capsys):
    log_file = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(log_file))

    res = log_event.enregistrer_evenement("Test event message")
    assert res is True
    assert log_file.exists()

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test event message" in captured.out

    content = log_file.read_text()
    assert "Test event message" in content

def test_enregistrer_evenement_log_injection(tmp_path, monkeypatch):
    log_file = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(log_file))

    res = log_event.enregistrer_evenement("Malicious Event\n[2025-01-01 00:00:00] Forged Admin Event")
    assert res is True

    lines = log_file.read_text().strip().split("\n")
    # Verify that newline was converted to space and entry is on a single line
    assert len(lines) == 1
    assert "Malicious Event [2025-01-01 00:00:00] Forged Admin Event" in lines[0]

def test_enregistrer_evenement_invalid_inputs(capsys):
    # Non-string input
    res = log_event.enregistrer_evenement(12345)
    assert res is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out

    # Empty / whitespace-only input
    res = log_event.enregistrer_evenement("   \n\r  ")
    assert res is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message ne peut pas être vide." in captured.out
