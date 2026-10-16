import os
import log_event

def test_enregistrer_evenement_injection_sanitisation(tmp_path, monkeypatch, capsys):
    log_file = tmp_path / "subdir" / "session_log.txt"

    real_open = open

    def mock_open(file, mode="r", *args, **kwargs):
        if "session_log.txt" in str(file) or file == "DATA/LOGS_SOUVERAINS/session_log.txt":
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            return real_open(log_file, mode, *args, **kwargs)
        return real_open(file, mode, *args, **kwargs)

    monkeypatch.setattr("builtins.open", mock_open)

    res = log_event.enregistrer_evenement("Injection attempt\n[2025-01-01 00:00:00] FAKE ADMIN LOG\r\nSecond line")
    assert res is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Injection attempt [2025-01-01 00:00:00] FAKE ADMIN LOG  Second line" in captured.out

    with real_open(log_file, "r") as f:
        lines = f.readlines()

    # Verify that newlines were stripped so it forms exactly ONE single log line entry
    assert len(lines) == 1
    assert "FAKE ADMIN LOG" in lines[0]
    assert "\n" not in lines[0][:-1]  # No inner newlines

def test_enregistrer_evenement_invalid_input(capsys):
    res = log_event.enregistrer_evenement(12345)
    assert res is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out
