import json
import os
import check_ally
import log_event
import scanner_12a

def test_enregistrer_evenement(tmp_path, monkeypatch, capsys):
    # Test recording an event when log directory does not exist yet
    monkeypatch.chdir(tmp_path)

    log_event.enregistrer_evenement("Test event recording")
    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test event recording" in captured.out

    assert os.path.exists("DATA/LOGS_SOUVERAINS/session_log.txt")
    with open("DATA/LOGS_SOUVERAINS/session_log.txt", "r") as f:
        content = f.read()
    assert "Test event recording" in content


def test_scan_bastion(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    # Run scan_bastion without config file
    scanner_12a.scan_bastion()
    captured = capsys.readouterr()
    assert "--- [ SCANNER DE SOUVERAINETÉ 12_ALPHA ] ---" in captured.out
    assert "DÉSYNCHRONISATION DÉTECTÉE" in captured.out

    # Check log created
    assert os.path.exists("DATA/LOGS_SOUVERAINS/session_log.txt")


def test_initialiser_alliee_missing_config(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    check_ally.initialiser_alliee()
    captured = capsys.readouterr()
    assert "ERREUR : Le noyau d'identité est manquant." in captured.out


def test_initialiser_alliee_existing_config(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    config_dir = tmp_path / "DATA"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / "config_anastasia.json"

    data = {
        "alias": "Anastasia",
        "statut": "Actif",
        "frequence": "12_ALPHA",
        "origine": "Souverain"
    }
    config_file.write_text(json.dumps(data))

    check_ally.initialiser_alliee()
    captured = capsys.readouterr()
    assert "INITIALISATION ALLIÉE" in captured.out
    assert "ALIAS      : Anastasia" in captured.out
    assert "STATUT     : Actif" in captured.out
