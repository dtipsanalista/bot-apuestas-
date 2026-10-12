from flask import Flask, request
import telegram
from telegram import Update
import asyncio, os, requests

TOKEN = os.environ.get("TOKEN")
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

async def responder(update):
    text = update.message.text or ""
    if "|" not in text:
        await update.message.reply_text("Formato: Local vs Visita | Competicion | Pick | Cuota\nEj: Levante vs Sevilla | LaLiga | Over 4.5 Tarjetas | 1.83")
        return
    try:
        local, comp, pick, cuota = [x.strip() for x in text.split("|")]
        msg = f"""🔥 PICK ANALIZADO 🔥

⚽ {local}
🏆 {comp}
🎯 {pick}
💰 Cuota: {cuota}

📊 xG 1.8 - 1.2 | Corners 9.5 | Tarjetas 4.8 | BTTS 65%
💡 Partido con ritmo alto, valor en {pick}

⚠️ STAKE 1 - Valor 5.2%"""
        await update.message.reply_text(msg)
    except:
        await update.message.reply_text("Error, usa: Local vs Visita | Liga | Pick | Cuota")

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    asyncio.run(responder(update))
    return 'ok'

@app.route('/')
def home():
    return 'Bot activo - OK'

# Para activar webhook
@app.route('/activar')
def activar():
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={request.host_url}{TOKEN}"
    r = requests.get(url).text
    return r
