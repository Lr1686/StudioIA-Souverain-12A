import check_ally
import log_event
import scanner_12a

def test_scan_bastion(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    # Create required files so scan_bastion checks pass
    (tmp_path / ".git").mkdir()
    data_dir = tmp_path / "DATA"
    data_dir.mkdir()
    (data_dir / "config_anastasia.json").write_text("{}")

    scanner_12a.scan_bastion()
    captured = capsys.readouterr()
    assert "SCANNER DE SOUVERAINETÉ 12_ALPHA" in captured.out
    assert "BASTION VERROUILLÉ ET ALIGNÉ ✅" in captured.out

    log_file = data_dir / "LOGS_SOUVERAINS" / "session_log.txt"
    assert log_file.exists()
    assert "Scan de souveraineté effectué" in log_file.read_text()

def test_enregistrer_evenement(tmp_path, monkeypatch, capsys):
    test_log_dir = tmp_path / "DATA" / "LOGS_SOUVERAINS"
    monkeypatch.chdir(tmp_path)

    log_event.enregistrer_evenement("Test event log")
    captured = capsys.readouterr()
    assert "ÉVÉNEMENT GRAVÉ : Test event log" in captured.out

    log_file = test_log_dir / "session_log.txt"
    assert log_file.exists()
    content = log_file.read_text()
    assert "Test event log" in content

def test_initialiser_alliee(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    # Test missing config
    check_ally.initialiser_alliee()
    captured = capsys.readouterr()
    assert "ERREUR : Le noyau d'identité est manquant." in captured.out

    # Test existing config
    data_dir = tmp_path / "DATA"
    data_dir.mkdir()
    config_file = data_dir / "config_anastasia.json"
    config_file.write_text('{"alias": "Anastasia", "statut": "Test", "frequence": "12_ALPHA", "origine": "TestPC"}')

    check_ally.initialiser_alliee()
    captured = capsys.readouterr()
    assert "INITIALISATION ALLIÉE" in captured.out
    assert "Anastasia" in captured.out
