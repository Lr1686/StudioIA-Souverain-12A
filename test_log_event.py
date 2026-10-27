import os
import log_event

def test_enregistrer_evenement_valid(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    res = log_event.enregistrer_evenement("Test event ok")
    assert res is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test event ok" in captured.out

    with open(test_log, "r") as f:
        content = f.read()
    assert "Test event ok" in content

def test_enregistrer_evenement_invalid_inputs(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Non-string input
    res = log_event.enregistrer_evenement(12345)
    assert res is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message de log doit être une chaîne de caractères." in captured.out

    # Empty input
    res = log_event.enregistrer_evenement("   ")
    assert res is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message de log ne peut pas être vide." in captured.out

    # Overly long input (>500 chars)
    res = log_event.enregistrer_evenement("A" * 501)
    assert res is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message dépasse la longueur maximale" in captured.out

    # Input containing newlines / log injection attempt
    res = log_event.enregistrer_evenement("System start\n[2026-03-30 00:00:00] Admin logged in")
    assert res is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message contient des caractères de contrôle non autorisés." in captured.out

    # Ensure log file was never created for invalid inputs
    assert not os.path.exists(test_log)
