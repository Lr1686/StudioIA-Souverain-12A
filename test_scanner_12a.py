import os
import scanner_12a


def test_scan_bastion_aligned(monkeypatch, capsys, tmp_path):
    log_dir = tmp_path / "DATA" / "LOGS_SOUVERAINS"
    log_dir.mkdir(parents=True, exist_ok=True)

    orig_exists = os.path.exists

    def mock_exists(path):
        if path in (".git", "DATA/config_anastasia.json"):
            return True
        return orig_exists(path)

    monkeypatch.setattr("os.path.exists", mock_exists)
    monkeypatch.setattr("os.listdir", lambda path: ["f1", "f2"])
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
        if path == ".git":
            return False
        if path == "DATA/config_anastasia.json":
            return True
        return orig_exists(path)

    monkeypatch.setattr("os.path.exists", mock_exists)
    monkeypatch.setattr("os.listdir", lambda path: ["f1"])
    monkeypatch.chdir(tmp_path)

    scanner_12a.scan_bastion()
    captured = capsys.readouterr()
    assert "ÉTAT       : DÉSYNCHRONISATION DÉTECTÉE ⚠️" in captured.out
    assert "↳ Manquant : Dépôt Git (.git) introuvable" in captured.out
    assert "Configuration" not in captured.out


def test_scan_bastion_desynchronized_missing_data(monkeypatch, capsys, tmp_path):
    log_dir = tmp_path / "DATA" / "LOGS_SOUVERAINS"
    log_dir.mkdir(parents=True, exist_ok=True)

    orig_exists = os.path.exists

    def mock_exists(path):
        if path == ".git":
            return True
        if path == "DATA/config_anastasia.json":
            return False
        return orig_exists(path)

    monkeypatch.setattr("os.path.exists", mock_exists)
    monkeypatch.setattr("os.listdir", lambda path: ["f1"])
    monkeypatch.chdir(tmp_path)

    scanner_12a.scan_bastion()
    captured = capsys.readouterr()
    assert "ÉTAT       : DÉSYNCHRONISATION DÉTECTÉE ⚠️" in captured.out
    assert "↳ Manquant : Configuration (DATA/config_anastasia.json) introuvable" in captured.out
    assert "Dépôt Git" not in captured.out
