import os
from flask import Flask, request
import requests
import random

app = Flask(__name__)
TOKEN = os.environ.get("TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}/"

def formatear_pick(partido, liga, mercado, cuota):
    xg1 = round(random.uniform(1.2, 2.1), 1)
    xg2 = round(random.uniform(0.8, 1.5), 1)
    corners = round(random.uniform(8.5, 11.5), 1)
    tarjetas = round(random.uniform(3.5, 5.5), 1)
    btts = random.randint(55, 75)
    valor = round(random.uniform(3.5, 6.5), 1)

    texto = f"""🔥 PICK ANALIZADO 🔥

⚽️ {partido}
🏆 {liga}
🎯 {mercado}
💰 Cuota: {cuota}

📊 xG {xg1} - {xg2} | Corners {corners} | Tarjetas {tarjetas} | BTTS {btts}%
💡 Partido con ritmo alto, valor en {mercado}

⚠️ STAKE 1 - Valor {valor}%"""
    return texto

@app.route('/', methods=['GET'])
def home():
    return "Bot funcionando!"

@app.route('/activar', methods=['GET'])
def activar():
    webhook = f"https://bot-apuestas-xmpu.onrender.com/webhook"
    r = requests.get(f"{URL}setWebhook?url={webhook}")
    return r.json()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        # Limpiar saltos de linea y espacios
        text_limpio = text.replace('\n', ' ').strip()

        if text_limpio.startswith('/'):
            msg = "Usa: Levante vs Sevilla | LaLiga | Over 4.5 Tarjetas | 1.83"
        else:
            try:
                partes = [p.strip() for p in text_limpio.split('|')]
                if len(partes) < 4:
                    raise ValueError
                partido = partes[0]
                liga = partes[1]
                mercado = partes[2]
                cuota = partes[3]
                msg = formatear_pick(partido, liga, mercado, cuota)
            except:
                msg = "Error, usa: Local vs Visita | Liga | Pick | Cuota"

        requests.post(f"{URL}sendMessage", json={"chat_id": chat_id, "text": msg})

    return {"ok": True}

if __name__ == '__main__':
    app.run()
