# Modulo dotenv para usar archivo .env
from dotenv import load_dotenv
load_dotenv()

import os

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
SECRET_KEY = os.getenv("TELEGRAM_BOT_API_KEY")

# Definimos algunos comandos básicos que funcionaran como handlers.

def start(update, context):
    """Manda un mensaje cuando el usuario ingresa /start """
    update.message.reply_text('Hola, bienvenido al BOT de Análisis Matemático!')


def ayuda(update, context):
    """Manda un mensaje cuando el usuario ingresa /ayuda """
    update.message.reply_text('Probá el comando /factoreo para recibir los casos más comunes de factoreo!')


def main():
    """Inicia el bot."""
    # Se crea un objeto Updater pasandole el token del bot
    updater = Updater(SECRET_KEY, use_context=True)

    # Obtenemos el dispatcher, del updater, para poder registrar los handlers (métodos)
    disp = updater.dispatcher

    # Para cada comando en telegram se asigna un handler
    disp.add_handler(CommandHandler("start", start))
    disp.add_handler(CommandHandler("ayuda", ayuda))

    # Inicia el Bot
    updater.start_polling()

    # Corre el bot hasta que se presione CTRL+C o el proceso reciba un SIGINT,
    # SIGTERM o SIGABRT.
    updater.idle()

if __name__ == '__main__':
    main()
