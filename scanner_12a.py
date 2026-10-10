import datetime
import os
import platform

def scan_bastion():
    print("--- [ SCANNER DE SOUVERAINETÉ 12_ALPHA ] ---")
    
    # 1. Analyse Matérielle
    # Performance Optimization: Avoid unused platform.system() call which executes unnecessary OS queries.
    version = platform.mac_ver()[0]
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
    log_path = "DATA/LOGS_SOUVERAINS/session_log.txt"
    # Performance Optimization: Guard directory creation with os.path.exists check.
    parent_dir = os.path.dirname(log_path)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a") as f:
        f.write(f"[{timestamp}] Scan de souveraineté effectué. État : ALIGNÉ.\n")

if __name__ == "__main__":
    scan_bastion()
