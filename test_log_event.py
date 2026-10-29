import os
import log_event
import scanner_12a

def test_enregistrer_evenement(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Test logging event when directory does not exist
    log_event.enregistrer_evenement("Test Event 1")
    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test Event 1" in captured.out
    assert os.path.exists(test_log)

    # Test logging event when directory already exists
    log_event.enregistrer_evenement("Test Event 2")

    with open(test_log, "r") as f:
        content = f.read()
    assert "Test Event 1" in content
    assert "Test Event 2" in content

def test_scan_bastion(tmp_path, monkeypatch, capsys):
    test_log_dir = tmp_path / "DATA" / "LOGS_SOUVERAINS"
    monkeypatch.chdir(tmp_path)

    scanner_12a.scan_bastion()
    captured = capsys.readouterr()
    assert "SCANNER DE SOUVERAINETÉ" in captured.out

    log_file = test_log_dir / "session_log.txt"
    assert os.path.exists(log_file)
    with open(log_file, "r") as f:
        content = f.read()
    assert "Scan de souveraineté effectué" in content
