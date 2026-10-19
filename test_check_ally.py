import json
import builtins
import check_ally

def test_initialiser_alliee_success(tmp_path, monkeypatch, capsys):
    config_file = tmp_path / "config_anastasia.json"
    config_data = {
        "alias": "AnastasiaTest",
        "statut": "Tester",
        "frequence": "99_ALPHA",
        "origine": "TestRunner"
    }
    config_file.write_text(json.dumps(config_data), encoding="utf-8")

    real_open = builtins.open
    def mock_open(path, mode="r", *args, **kwargs):
        if str(path) == "DATA/config_anastasia.json":
            return real_open(config_file, mode, *args, **kwargs)
        return real_open(path, mode, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", mock_open)

    check_ally.initialiser_alliee()
    captured = capsys.readouterr()

    assert "--- [ INITIALISATION ALLIÉE ] ---" in captured.out
    assert "ALIAS      : AnastasiaTest" in captured.out
    assert "STATUT     : Tester" in captured.out
    assert "FRÉQUENCE  : 99_ALPHA" in captured.out
    assert "Souveraineté confirmée via TestRunner" in captured.out

def test_initialiser_alliee_missing_file(monkeypatch, capsys):
    def mock_open_missing(path, mode="r", *args, **kwargs):
        raise FileNotFoundError()

    monkeypatch.setattr(builtins, "open", mock_open_missing)

    check_ally.initialiser_alliee()
    captured = capsys.readouterr()

    assert "ERREUR : Le noyau d'identité est manquant." in captured.out
