import check_ally

def test_initialiser_alliee_success(tmp_path, monkeypatch, capsys):
    data_dir = tmp_path / "DATA"
    data_dir.mkdir()
    config_file = data_dir / "config_anastasia.json"
    config_file.write_text('{"alias": "TestAlias", "statut": "Active", "frequence": "432Hz", "origine": "Lab"}')

    # Change directory to temporary path
    monkeypatch.chdir(tmp_path)

    check_ally.initialiser_alliee()
    captured = capsys.readouterr()
    assert "ALIAS      : TestAlias" in captured.out
    assert "STATUT     : Active" in captured.out
    assert "FRÉQUENCE  : 432Hz" in captured.out
    assert "Souveraineté confirmée via Lab" in captured.out

def test_initialiser_alliee_missing_file(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    check_ally.initialiser_alliee()
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le noyau d'identité est manquant (DATA/config_anastasia.json)." in captured.out
