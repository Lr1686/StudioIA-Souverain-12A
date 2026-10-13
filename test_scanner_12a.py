import os
import scanner_12a

def test_scan_bastion(monkeypatch, tmp_path, capsys):
    # Change working directory to tmp_path
    monkeypatch.chdir(tmp_path)

    # Create dummy files and directories
    (tmp_path / "file1.txt").touch()
    (tmp_path / "file2.txt").touch()
    (tmp_path / ".git").mkdir()

    data_dir = tmp_path / "DATA"
    data_dir.mkdir()
    (data_dir / "config_anastasia.json").touch()

    scanner_12a.scan_bastion()
    captured = capsys.readouterr()

    # .git, file1.txt, file2.txt, DATA -> 4 items
    assert "CAPACITÉ   : 4 artefacts détectés" in captured.out
    assert "ÉTAT       : BASTION VERROUILLÉ ET ALIGNÉ ✅" in captured.out

    # Check log file created
    log_file = tmp_path / "DATA" / "LOGS_SOUVERAINS" / "session_log.txt"
    assert log_file.exists()
    assert "Scan de souveraineté effectué" in log_file.read_text()

def test_scan_bastion_desynchronized(monkeypatch, tmp_path, capsys):
    monkeypatch.chdir(tmp_path)

    (tmp_path / "file1.txt").touch()

    scanner_12a.scan_bastion()
    captured = capsys.readouterr()

    assert "CAPACITÉ   : 1 artefacts détectés" in captured.out
    assert "ÉTAT       : DÉSYNCHRONISATION DÉTECTÉE ⚠️" in captured.out
