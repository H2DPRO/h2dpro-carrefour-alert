import pandas as pd
import requests
from pathlib import Path

SEUIL_PRIX = 30.0

TELEGRAM_TOKEN = "8525996715:AAGTE6GlMOYxeqn_wPc4jHNvWzy9V6HsIJM"
TELEGRAM_CHAT_ID = "-5239164901"

CSV_FILE = "carrefour-dolce-test.csv"
LAST_PRICE_FILE = Path("last_price.txt")

# ------------------------
# LECTURE PRIX ACTUEL
# ------------------------

df = pd.read_csv(CSV_FILE)

prix_str = df.iloc[0]["price"]

# Nettoyage complet du prix
clean = prix_str.replace("€", "")
clean = clean.replace(",", ".")
clean = clean.replace(" ", "")
prix = float(clean)

print("Prix détecté :", prix)

# ------------------------
# LECTURE DERNIER PRIX
# ------------------------

if LAST_PRICE_FILE.exists():
    dernier_prix = float(LAST_PRICE_FILE.read_text())
else:
    dernier_prix = None

print("Dernier prix :", dernier_prix)

# ------------------------
# CONDITIONS ALERTE
# ------------------------

envoyer_alerte = False

if dernier_prix is None:
    if prix <= SEUIL_PRIX:
        envoyer_alerte = True
elif prix != dernier_prix and prix <= SEUIL_PRIX:
    envoyer_alerte = True

# ------------------------
# ENVOI TELEGRAM
# ------------------------

if envoyer_alerte:

    message = "ALERTE PRIX CARREFOUR\n\n"
    message += "Nouveau prix : " + str(prix) + " €\n"
    message += "Ancien prix : " + str(dernier_prix)

    url = "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    response = requests.post(url, data=payload)
    print("Réponse Telegram :", response.text)

else:
    print("Pas d'alerte envoyée.")

# ------------------------
# MISE À JOUR MÉMOIRE
# ------------------------

LAST_PRICE_FILE.write_text(str(prix))
print("last_price.txt mis à jour.")
