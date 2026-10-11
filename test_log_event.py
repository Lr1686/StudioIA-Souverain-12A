import os
import log_event

def test_enregistrer_evenement_success(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement("Test event log message")
    assert result is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test event log message" in captured.out

    with open(test_log, "r") as f:
        lines = f.readlines()
    assert len(lines) == 1
    assert "Test event log message\n" in lines[0]

def test_enregistrer_evenement_invalid_inputs(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Empty message
    assert log_event.enregistrer_evenement("   ") is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message ne peut pas être vide." in captured.out

    # Overly long message
    assert log_event.enregistrer_evenement("A" * 501) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message dépasse la longueur maximale autorisée" in captured.out

    # Log injection / newline / control character attempt
    assert log_event.enregistrer_evenement("Valid message\n[2026-01-01 00:00:00] Fake admin event") is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message contient des caractères de contrôle non autorisés." in captured.out

    # Non-string input
    assert log_event.enregistrer_evenement(12345) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out
