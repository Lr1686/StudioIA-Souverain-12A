import os
import log_event

def test_enregistrer_evenement_success(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement("Événement de test réussi")
    assert result is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Événement de test réussi" in captured.out

    assert os.path.exists(test_log)
    with open(test_log, "r") as f:
        content = f.read()
    assert "Événement de test réussi" in content

def test_enregistrer_evenement_log_injection_sanitization(tmp_path, monkeypatch):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    injected_message = "Valid message\n[2026-01-01 00:00:00] FAKE INJECTED LOG ENTRY"
    result = log_event.enregistrer_evenement(injected_message)
    assert result is True

    with open(test_log, "r") as f:
        lines = f.readlines()

    # Log forging check: Injected newlines should be replaced by spaces, maintaining exactly 1 line
    assert len(lines) == 1
    assert "FAKE INJECTED LOG ENTRY" in lines[0]
    assert "\n" not in lines[0][:-1]  # No inner newline character

def test_enregistrer_evenement_invalid_inputs(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Empty string
    assert log_event.enregistrer_evenement("   ") is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message ne peut pas être vide." in captured.out

    # Non-string input
    assert log_event.enregistrer_evenement(12345) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out

    # Exceeding length limit (> 500 chars)
    long_msg = "X" * 501
    assert log_event.enregistrer_evenement(long_msg) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message dépasse la longueur maximale autorisée" in captured.out
