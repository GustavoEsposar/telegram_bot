from telethon import TelegramClient, events
import requests
import os

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))
CRITERIO = os.getenv("CRITERIO", "uber")

# Nome da sessão do Telethon
client = TelegramClient('userbot', api_id, api_hash)

def enviar_para_bot(mensagem):
    """Envia a mensagem filtrada para o bot, que encaminha para CHAT_ID"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": mensagem
    }
    try:
        response = requests.post(url, data=data)
        if response.status_code != 200:
            print("Erro ao enviar mensagem pelo bot:", response.text)
    except Exception as e:
        print("Exceção ao enviar mensagem:", e)

@client.on(events.NewMessage)
async def handler(event):
    chat = await event.get_chat()
    msg = event.message.message

    # Apenas filtra mensagens de grupos ou canais
    if event.is_group or event.is_channel:
        # Checa se a mensagem contém a palavra-chave
        if CRITERIO.lower() in msg.lower():
            print(f"[{chat.title}] {msg}")
            # Encaminha para o bot
            enviar_para_bot(f"[{chat.title}] {msg}")

print("Userbot rodando...")
client.start()  # primeiro login pedirá código SMS/Telegram
client.run_until_disconnected()
