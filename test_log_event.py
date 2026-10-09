import log_event

def test_enregistrer_evenement_success(tmp_path, monkeypatch, capsys):
    test_log_path = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log_path))

    res = log_event.enregistrer_evenement("Test message valid")
    assert res is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test message valid" in captured.out

    lines = test_log_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    assert "Test message valid" in lines[0]


def test_enregistrer_evenement_log_injection_prevention(tmp_path, monkeypatch):
    test_log_path = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log_path))

    # Injection attempt with newline and forged log entry
    malicious_input = "User action\n[2026-01-01 00:00:00] Admin access granted"
    res = log_event.enregistrer_evenement(malicious_input)
    assert res is True

    lines = test_log_path.read_text(encoding="utf-8").splitlines()
    # Must remain on 1 single line due to newline neutralization
    assert len(lines) == 1
    assert "\n" not in lines[0]


def test_enregistrer_evenement_validation_errors(tmp_path, monkeypatch, capsys):
    test_log_path = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log_path))

    # Non-string input
    assert log_event.enregistrer_evenement(12345) is False
    assert "⚠️ ERREUR : Le message de log doit être une chaîne de caractères." in capsys.readouterr().out

    # Empty / whitespace-only message
    assert log_event.enregistrer_evenement("   ") is False
    assert "⚠️ ERREUR : Le message de log ne peut pas être vide." in capsys.readouterr().out

    # Overly long message (>1000 chars)
    long_msg = "A" * 1001
    assert log_event.enregistrer_evenement(long_msg) is False
    assert "⚠️ ERREUR : Le message dépasse la longueur maximale" in capsys.readouterr().out
