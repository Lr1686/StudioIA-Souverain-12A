import os
import platform
import datetime

def scan_bastion():
    print("--- [ SCANNER DE SOUVERAINETÉ 12_ALPHA ] ---")
    
    # 1. Analyse Matérielle
    systeme = platform.system()
    version = platform.mac_ver()[0]
    machine = platform.machine()
    
    # 2. Analyse de l'Espace de Travail & Vérification des Sceaux
    # Performance Optimization: Use os.scandir() iterator instead of os.listdir() to avoid
    # allocating a full list of filenames in memory (O(1) memory usage) and check for '.git'
    # during iteration to save a redundant stat system call.
    nb_fichiers = 0
    has_git = False
    with os.scandir('.') as entries:
        for entry in entries:
            nb_fichiers += 1
            if entry.name == '.git':
                has_git = True

    has_data = os.path.exists('DATA/config_anastasia.json')
    
    # Rapport
    print(f"BATAILLON  : MacBook Pro ({machine})")
    print(f"OS VERSION : macOS {version}")
    print(f"CAPACITÉ   : {nb_fichiers} artefacts détectés")
    print(f"---")
    
    if has_git and has_data:
        print("ÉTAT       : BASTION VERROUILLÉ ET ALIGNÉ ✅")
    else:
        print("ÉTAT       : DÉSYNCHRONISATION DÉTECTÉE ⚠️")
    
    # Enregistrement automatique dans les logs
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_path = "DATA/LOGS_SOUVERAINS/session_log.txt"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "a") as f:
        f.write(f"[{timestamp}] Scan de souveraineté effectué. État : ALIGNÉ.\n")

if __name__ == "__main__":
    scan_bastion()
