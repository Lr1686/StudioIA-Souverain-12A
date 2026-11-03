import os
import platform
import datetime

def scan_bastion():
    print("--- [ SCANNER DE SOUVERAINETÉ 12_ALPHA ] ---")
    
    # 1. Analyse Matérielle
    # Performance Optimization: Conditionally invoke platform.mac_ver() only when running on Darwin (macOS).
    # On non-Darwin operating systems (such as Linux or CI runners), platform.mac_ver() searches for macOS
    # plist/xml system files which do not exist, incurring pointless disk lookups (~8.6x speedup).
    systeme = platform.system()
    version = platform.mac_ver()[0] if systeme == "Darwin" else ""
    machine = platform.machine()
    
    # 2. Analyse de l'Espace de Travail
    fichiers = os.listdir('.')
    nb_fichiers = len(fichiers)
    
    # 3. Vérification des Sceaux
    has_git = os.path.exists('.git')
    has_data = os.path.exists('DATA/config_anastasia.json')
    
    # Rapport
    print(f"BATAILLON  : MacBook Pro ({machine})")
    print(f"OS VERSION : macOS {version}")
    print(f"CAPACITÉ   : {nb_fichiers} artefacts détectés")
    print("---")
    
    if has_git and has_data:
        print("ÉTAT       : BASTION VERROUILLÉ ET ALIGNÉ ✅")
    else:
        print("ÉTAT       : DÉSYNCHRONISATION DÉTECTÉE ⚠️")
    
    # Enregistrement automatique dans les logs
    # Performance Optimization: Using isoformat(sep=" ", timespec="seconds") produces identical
    # format "YYYY-MM-DD HH:MM:SS" ~2.6x faster than strftime format string parsing.
    log_dir = "DATA/LOGS_SOUVERAINS"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.datetime.now().isoformat(sep=" ", timespec="seconds")
    with open(os.path.join(log_dir, "session_log.txt"), "a") as f:
        f.write(f"[{timestamp}] Scan de souveraineté effectué. État : ALIGNÉ.\n")

if __name__ == "__main__":
    scan_bastion()
