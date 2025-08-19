from telethon import TelegramClient, events
import requests
import os
import asyncio
from flask import Flask
import threading

# --- Variáveis de ambiente ---
api_id = int(os.getenv("API_ID", ""))
api_hash = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", ":")
CHAT_ID = int(os.getenv("CHAT_ID", ""))
CRITERIO = os.getenv("CRITERIO", "uber")

# --- Telethon ---
client = TelegramClient('userbot', api_id, api_hash)

def enviar_para_bot(mensagem):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": mensagem}
    try:
        r = requests.post(url, data=data)
        if r.status_code != 200:
            print("Erro ao enviar:", r.text)
    except Exception as e:
        print("Exceção ao enviar:", e)

@client.on(events.NewMessage)
async def handler(event):
    chat = await event.get_chat()
    msg = event.message.message or ""

    if event.is_group or event.is_channel:
        if CRITERIO.lower() in msg.lower():
            print(f"[{chat.title}] {msg}")
            enviar_para_bot(f"[{chat.title}] {msg}")

# --- Flask (mantém vivo no Render) ---
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot rodando no Render 🚀"

def iniciar_flask():
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))

async def iniciar_telethon():
    await client.start()
    print("Telethon iniciado ✅")
    await client.run_until_disconnected()

if __name__ == "__main__":
    # roda Flask em thread paralela
    threading.Thread(target=iniciar_flask).start()
    # roda Telethon no loop principal
    asyncio.run(iniciar_telethon())
