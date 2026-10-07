import log_event

def test_enregistrer_evenement(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    test_log.parent.mkdir(parents=True, exist_ok=True)

    # Patch log_path to use tmp_path
    monkeypatch.setattr(log_event, "enregistrer_evenement", lambda msg: _test_log(msg, str(test_log), capsys))

def _test_log(message, log_path, capsys):
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}\n"
    with open(log_path, "a") as f:
        f.write(entry)
    print(f"🔱 ÉVÉNEMENT GRAVÉ : {message}")

def test_enregistrer_evenement_direct(tmp_path, capsys):
    log_dir = tmp_path / "DATA" / "LOGS_SOUVERAINS"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "session_log.txt"

    # Save original working dir and change to tmp_path
    import os
    orig_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        log_event.enregistrer_evenement("Test message")
        captured = capsys.readouterr()
        assert "🔱 ÉVÉNEMENT GRAVÉ : Test message" in captured.out
        assert log_file.exists()
        content = log_file.read_text()
        assert "Test message" in content
    finally:
        os.chdir(orig_cwd)
