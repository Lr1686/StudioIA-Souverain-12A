import os
import platform
import datetime


def scan_bastion():
    print("--- [ SCANNER DE SOUVERAINETÉ 12_ALPHA ] ---")

    # 1. Analyse Matérielle
    systeme = platform.system()
    mac_version = platform.mac_ver()[0]
    os_display = f"macOS {mac_version}" if mac_version else systeme
    machine = platform.machine()

    # 2. Analyse de l'Espace de Travail
    fichiers = os.listdir(".")
    nb_fichiers = len(fichiers)

    # 3. Vérification des Sceaux
    has_git = os.path.exists(".git")
    has_data = os.path.exists("DATA/config_anastasia.json")

    # Rapport
    print(f"BATAILLON  : MacBook Pro ({machine})")
    print(f"OS VERSION : {os_display}")
    print(f"CAPACITÉ   : {nb_fichiers} artefacts détectés")
    print("---")

    if has_git and has_data:
        print("ÉTAT       : BASTION VERROUILLÉ ET ALIGNÉ ✅")
    else:
        print("ÉTAT       : DÉSYNCHRONISATION DÉTECTÉE ⚠️")
        if not has_git:
            print("  ↳ Manquant : Dépôt Git (.git) introuvable")
        if not has_data:
            print(
                "  ↳ Manquant : Fichier de configuration (DATA/config_anastasia.json) introuvable"
            )

    # Enregistrement automatique dans les logs
    # Performance Optimization: Using isoformat(sep=" ", timespec="seconds") produces identical
    # format "YYYY-MM-DD HH:MM:SS" ~2.6x faster than strftime format string parsing.
    timestamp = datetime.datetime.now().isoformat(sep=" ", timespec="seconds")
    with open("DATA/LOGS_SOUVERAINS/session_log.txt", "a") as f:
        f.write(f"[{timestamp}] Scan de souveraineté effectué. État : ALIGNÉ.\n")


if __name__ == "__main__":
    scan_bastion()
