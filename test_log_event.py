import os
import log_event

def test_enregistrer_evenement_valid(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement("Événement de test")
    assert result is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Événement de test" in captured.out

    assert os.path.exists(test_log)
    with open(test_log, "r") as f:
        content = f.read()
    assert "Événement de test" in content

def test_enregistrer_evenement_invalid_type(capsys):
    result = log_event.enregistrer_evenement(12345)
    assert result is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out

def test_enregistrer_evenement_empty(capsys):
    result = log_event.enregistrer_evenement("   ")
    assert result is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message ne peut pas être vide." in captured.out

def test_enregistrer_evenement_max_length(capsys):
    result = log_event.enregistrer_evenement("A" * 1001)
    assert result is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message dépasse la longueur maximale autorisée" in captured.out

def test_enregistrer_evenement_log_injection_sanitisation(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Injection with newlines
    result = log_event.enregistrer_evenement("Normal event\n[2026-01-01 00:00:00] FORGED LOG ENTRY")
    assert result is True

    with open(test_log, "r") as f:
        lines = f.readlines()

    # Check that it didn't create a second line in the log file
    assert len(lines) == 1
    assert "\n" not in lines[0][:-1]  # No inner newline
