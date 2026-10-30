import os
import log_event

def test_enregistrer_evenement(tmp_path, monkeypatch, capsys):
    log_dir = tmp_path / "LOGS_SOUVERAINS"
    log_file = log_dir / "session_log.txt"

    # We test `enregistrer_evenement` directly after patching the module-level default path if we refactor or patch the path inside the module
    # Let's test calling `enregistrer_evenement` by temporarily changing working dir or patching log file path if module allows, or patching open/path.
    # To test accurately without monkeypatching logic:
    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        log_event.enregistrer_evenement("Test event 1")
        captured = capsys.readouterr()
        assert "🔱 ÉVÉNEMENT GRAVÉ : Test event 1" in captured.out

        actual_log = tmp_path / "DATA" / "LOGS_SOUVERAINS" / "session_log.txt"
        assert actual_log.exists()
        content = actual_log.read_text()
        assert "Test event 1" in content
    finally:
        os.chdir(cwd)
