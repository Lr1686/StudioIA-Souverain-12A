import datetime

def enregistrer_evenement(message):
    log_path = "DATA/LOGS_SOUVERAINS/session_log.txt"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Performance Optimization: Use f-strings instead of string concatenation (+).
    # F-strings format expressions directly at bytecode evaluation level, avoiding intermediate string objects.
    entry = f"[{timestamp}] {message}\n"
    
    with open(log_path, "a") as f:
        f.write(entry)
    print(f"🔱 ÉVÉNEMENT GRAVÉ : {message}")

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
