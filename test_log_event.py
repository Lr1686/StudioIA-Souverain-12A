import log_event

def test_enregistrer_evenement_sanitization(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    # Test multiline log message (log injection attempt CWE-117)
    malicious_input = "User login successful\n[2025-01-01 00:00:00] [CRITICAL] Fake Admin Logged In\r[2025-01-01 00:00:00] Injected"
    log_event.enregistrer_evenement(malicious_input)

    log_file = tmp_path / "DATA" / "LOGS_SOUVERAINS" / "session_log.txt"
    assert log_file.exists()

    content = log_file.read_text()
    lines = [line for line in content.splitlines() if line]

    # Should be recorded as a single line, preventing newline log forging
    assert len(lines) == 1
    assert "User login successful [2025-01-01 00:00:00] [CRITICAL] Fake Admin Logged In [2025-01-01 00:00:00] Injected" in lines[0]

def test_enregistrer_evenement_creates_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    # Verify directory does not exist initially
    log_dir = tmp_path / "DATA" / "LOGS_SOUVERAINS"
    assert not log_dir.exists()

    # Log event should create parent directory automatically
    log_event.enregistrer_evenement("Normal log message")

    assert log_dir.exists()
    log_file = log_dir / "session_log.txt"
    assert log_file.exists()
    assert "Normal log message" in log_file.read_text()
