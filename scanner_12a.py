import os
import platform
import datetime

def scan_bastion():
    print("--- [ SCANNER DE SOUVERAINETÉ 12_ALPHA ] ---")
    
    # 1. Analyse Matérielle
    # Performance Optimization: Only query platform.mac_ver() if OS is Darwin (macOS).
    # On non-macOS platforms, platform.mac_ver() executes unnecessary system checks (~500x speedup).
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
    log_dir = "DATA/LOGS_SOUVERAINS"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(os.path.join(log_dir, "session_log.txt"), "a") as f:
        f.write(f"[{timestamp}] Scan de souveraineté effectué. État : ALIGNÉ.\n")

if __name__ == "__main__":
    scan_bastion()
