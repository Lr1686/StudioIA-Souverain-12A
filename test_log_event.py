import os
import log_event

def test_enregistrer_evenement_non_existing_and_existing_dir(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "NEW_LOGS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # 1. First call when directory does not exist (triggers FileNotFoundError -> os.makedirs)
    log_event.enregistrer_evenement("Premier message (dossier absent)")
    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Premier message (dossier absent)" in captured.out
    assert test_log.exists()
    assert "Premier message (dossier absent)" in test_log.read_text()

    # 2. Second call when directory exists (direct append without makedirs overhead)
    log_event.enregistrer_evenement("Second message (dossier présent)")
    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Second message (dossier présent)" in captured.out
    content = test_log.read_text()
    assert "Premier message (dossier absent)" in content
    assert "Second message (dossier présent)" in content
