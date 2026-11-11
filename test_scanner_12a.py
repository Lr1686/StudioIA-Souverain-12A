import os
import scanner_12a


def test_scan_bastion_aligned(capsys):
    scanner_12a.scan_bastion()
    captured = capsys.readouterr()
    assert "--- [ SCANNER DE SOUVERAINETÉ 12_ALPHA ] ---" in captured.out
    assert "SCEAU GIT  : ALIGNÉ ✅" in captured.out
    assert "SCEAU DATA : ALIGNÉ ✅" in captured.out
    assert "ÉTAT       : BASTION VERROUILLÉ ET ALIGNÉ ✅" in captured.out


def test_scan_bastion_desynchronized(monkeypatch, capsys):
    # Mock os.path.exists to simulate missing config and git
    original_exists = os.path.exists

    def mock_exists(path):
        if path in ('.git', 'DATA/config_anastasia.json'):
            return False
        return original_exists(path)

    monkeypatch.setattr(os.path, "exists", mock_exists)
    scanner_12a.scan_bastion()
    captured = capsys.readouterr()
    assert "SCEAU GIT  : MANQUANT (.git) ❌" in captured.out
    assert "SCEAU DATA : MANQUANT (config_anastasia.json) ❌" in captured.out
    assert "ÉTAT       : DÉSYNCHRONISATION DÉTECTÉE ⚠️" in captured.out
