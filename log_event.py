import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"

def enregistrer_evenement(message):
    if not isinstance(message, str):
        print("⚠️ ERREUR : Le message de log doit être une chaîne de caractères.")
        return False

    msg_clean = message.strip()
    if not msg_clean:
        print("⚠️ ERREUR : Le message de log ne peut pas être vide.")
        return False

    # Validation de sécurité : éviter l'injection de logs (CWE-117) via retours à la ligne ou caractères de contrôle
    if any(ord(c) < 32 or ord(c) == 127 for c in msg_clean):
        print("⚠️ ERREUR : Le message contient des caractères non autorisés ou retours à la ligne.")
        return False

    log_dir = os.path.dirname(LOG_PATH)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {msg_clean}\n"

    with open(LOG_PATH, "a") as f:
        f.write(entry)
    print(f"🔱 ÉVÉNEMENT GRAVÉ : {msg_clean}")
    return True

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
