import log_event

def test_enregistrer_evenement_normal(tmp_path, monkeypatch, capsys):
    log_file = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(log_file))

    log_event.enregistrer_evenement("Test message normal")
    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test message normal" in captured.out

    assert log_file.exists()
    content = log_file.read_text()
    assert "Test message normal" in content

def test_enregistrer_evenement_creates_dir(tmp_path, monkeypatch):
    nested_dir = tmp_path / "LOGS_SUBDIR"
    log_file = nested_dir / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(log_file))

    assert not nested_dir.exists()
    log_event.enregistrer_evenement("Test directory creation")
    assert nested_dir.exists()
    assert log_file.exists()

def test_enregistrer_evenement_log_injection_sanitization(tmp_path, monkeypatch):
    log_file = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(log_file))

    # Test newline injection attempt
    malicious_msg = "User logged in\n[2026-01-01 00:00:00] Admin access granted\r\nFake line"
    log_event.enregistrer_evenement(malicious_msg)

    content = log_file.read_text()
    lines = content.strip().split("\n")
    # Must be recorded as a single log line, not forged into multiple lines
    assert len(lines) == 1
    assert "User logged in [2026-01-01 00:00:00] Admin access granted Fake line" in lines[0]

def test_enregistrer_evenement_length_truncation(tmp_path, monkeypatch):
    log_file = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(log_file))

    long_msg = "A" * 1500
    log_event.enregistrer_evenement(long_msg)

    content = log_file.read_text()
    assert "... [TRUNCATED]" in content
    assert len(content.strip().split("] ")[1]) < 1100

def test_enregistrer_evenement_non_string_input(tmp_path, monkeypatch):
    log_file = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(log_file))

    log_event.enregistrer_evenement(123456)
    content = log_file.read_text()
    assert "123456" in content
