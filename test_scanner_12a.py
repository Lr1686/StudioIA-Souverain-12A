import os
import scanner_12a

def test_scan_bastion_aligned(monkeypatch, capsys, tmp_path):
    # Setup log directory mock
    log_dir = tmp_path / "DATA" / "LOGS_SOUVERAINS"
    log_dir.mkdir(parents=True, exist_ok=True)

    orig_exists = os.path.exists

    def mock_exists(path):
        if path in ('.git', 'DATA/config_anastasia.json'):
            return True
        return orig_exists(path)

    monkeypatch.setattr("os.path.exists", mock_exists)
    monkeypatch.setattr("os.listdir", lambda path: ["f1", "f2"])

    # Redirect log output file to tmp_path
    monkeypatch.chdir(tmp_path)

    scanner_12a.scan_bastion()
    captured = capsys.readouterr()
    assert "ÉTAT       : BASTION VERROUILLÉ ET ALIGNÉ ✅" in captured.out
    assert "DÉSYNCHRONISATION" not in captured.out

def test_scan_bastion_desynchronized_missing_git(monkeypatch, capsys, tmp_path):
    log_dir = tmp_path / "DATA" / "LOGS_SOUVERAINS"
    log_dir.mkdir(parents=True, exist_ok=True)

    orig_exists = os.path.exists

    def mock_exists(path):
        if path == '.git':
            return False
        if path == 'DATA/config_anastasia.json':
            return True
        return orig_exists(path)

    monkeypatch.setattr("os.path.exists", mock_exists)
    monkeypatch.setattr("os.listdir", lambda path: ["f1"])
    monkeypatch.chdir(tmp_path)

    scanner_12a.scan_bastion()
    captured = capsys.readouterr()
    assert "ÉTAT       : DÉSYNCHRONISATION DÉTECTÉE ⚠️" in captured.out
    assert "Dépôt Git non initialisé (.git)" in captured.out

def test_scan_bastion_desynchronized_missing_data(monkeypatch, capsys, tmp_path):
    log_dir = tmp_path / "DATA" / "LOGS_SOUVERAINS"
    log_dir.mkdir(parents=True, exist_ok=True)

    orig_exists = os.path.exists

    def mock_exists(path):
        if path == '.git':
            return True
        if path == 'DATA/config_anastasia.json':
            return False
        return orig_exists(path)

    monkeypatch.setattr("os.path.exists", mock_exists)
    monkeypatch.setattr("os.listdir", lambda path: ["f1"])
    monkeypatch.chdir(tmp_path)

    scanner_12a.scan_bastion()
    captured = capsys.readouterr()
    assert "ÉTAT       : DÉSYNCHRONISATION DÉTECTÉE ⚠️" in captured.out
    assert "Fichier de configuration absent (DATA/config_anastasia.json)" in captured.out
