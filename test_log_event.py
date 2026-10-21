import os
import log_event

def test_enregistrer_evenement_succes(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    res = log_event.enregistrer_evenement("Événement de test réussi")
    assert res is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Événement de test réussi" in captured.out

    assert os.path.exists(test_log)
    with open(test_log, "r") as f:
        lines = f.readlines()
    assert len(lines) == 1
    assert "Événement de test réussi" in lines[0]

def test_enregistrer_evenement_log_injection(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Attempting log injection via newlines
    malicious_msg = "Alerte normale\n[2026-01-01 00:00:00] Infiltration réussie"
    res = log_event.enregistrer_evenement(malicious_msg)
    assert res is True

    # The log file should contain exactly 1 log line with newlines replaced by spaces
    with open(test_log, "r") as f:
        lines = f.readlines()
    assert len(lines) == 1
    assert "Infiltration réussie" in lines[0]
    assert "\n[2026-01-01" not in lines[0]

def test_enregistrer_evenement_invalid_inputs(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Non-string input
    assert log_event.enregistrer_evenement(12345) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out

    # Empty input
    assert log_event.enregistrer_evenement("   ") is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message ne peut pas être vide." in captured.out

    # Overly long input (>1000 chars)
    assert log_event.enregistrer_evenement("A" * 1001) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message dépasse la longueur maximale autorisée" in captured.out
