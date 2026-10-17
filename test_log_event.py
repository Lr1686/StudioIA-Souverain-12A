import os
import log_event

def test_enregistrer_evenement_normal(tmp_path, monkeypatch, capsys):
    log_file = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(log_file))

    res = log_event.enregistrer_evenement("Test normal message")
    assert res is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test normal message" in captured.out

    with open(log_file, "r") as f:
        content = f.read()
    assert "Test normal message" in content

def test_enregistrer_evenement_log_injection_sanitization(tmp_path, monkeypatch):
    log_file = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(log_file))

    # Injection attempt with fake log line and newlines
    malicious_msg = "User logged in\n[2026-03-30 12:00:00] [ADMIN] Granted superuser privileges\r\nFake line"
    res = log_event.enregistrer_evenement(malicious_msg)
    assert res is True

    with open(log_file, "r") as f:
        lines = f.readlines()

    # Should be exactly 1 line logged because newlines were sanitized
    assert len(lines) == 1
    assert "\n" not in lines[0][:-1]
    assert "Granted superuser privileges" in lines[0]

def test_enregistrer_evenement_invalid_type():
    res = log_event.enregistrer_evenement(12345)
    assert res is False

def test_enregistrer_evenement_directory_creation(tmp_path, monkeypatch):
    nested_log_file = tmp_path / "sub_dir" / "logs" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(nested_log_file))

    res = log_event.enregistrer_evenement("Directory creation test")
    assert res is True
    assert os.path.exists(nested_log_file)
