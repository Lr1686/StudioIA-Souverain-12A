from unittest.mock import mock_open
import scanner_12a


def test_scan_bastion_aligned(monkeypatch, capsys):
    m_open = mock_open()
    monkeypatch.setattr(scanner_12a, "open", m_open, raising=False)

    # Mock seals present
    monkeypatch.setattr(
        scanner_12a.os.path,
        "exists",
        lambda path: True if path in (".git", "DATA/config_anastasia.json") else False,
    )

    scanner_12a.scan_bastion()
    captured = capsys.readouterr()

    assert "SCEAU GIT  : ALIGNÉ ✅" in captured.out
    assert "SCEAU DATA : ALIGNÉ ✅" in captured.out
    assert "ÉTAT       : BASTION VERROUILLÉ ET ALIGNÉ ✅" in captured.out

    # Verify log write was performed
    m_open().write.assert_called_once()
    written_log = m_open().write.call_args[0][0]
    assert "Scan de souveraineté effectué. État : ALIGNÉ." in written_log


def test_scan_bastion_missing_seals(monkeypatch, capsys):
    m_open = mock_open()
    monkeypatch.setattr(scanner_12a, "open", m_open, raising=False)

    # Mock git seal present, but data seal missing
    monkeypatch.setattr(
        scanner_12a.os.path,
        "exists",
        lambda path: True if path == ".git" else False,
    )

    scanner_12a.scan_bastion()
    captured = capsys.readouterr()

    assert "SCEAU GIT  : ALIGNÉ ✅" in captured.out
    assert "SCEAU DATA : MANQUANT ⚠️" in captured.out
    assert "ÉTAT       : DÉSYNCHRONISATION DÉTECTÉE ⚠️" in captured.out
