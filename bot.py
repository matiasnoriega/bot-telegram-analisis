import os

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Declaramos algunas variables necesarias para el Bot
PORT = int(os.environ.get('PORT', 5000))
SECRET_KEY = os.environ['TELEGRAM_BOT_API_KEY']
HEROKU_APP = os.environ['HEROKU_APP']

# Definimos algunos comandos básicos que funcionaran como handlers.

def saludo(update, context):
    """Manda un mensaje cuando el usuario ingresa /saludo """
    update.message.reply_text('Hola! Soy el BOT de Análisis Matemático! Sirvo como un ayuda-memoria para la cursada')

def factoreo(update, context):
    """ Devuelve tabla de casos mas comunes de factoreo """
    update.message.reply_photo(photo=open('assets/factoreo.png', 'rb'))

def ayuda(update, context):
    """Manda un mensaje cuando el usuario ingresa /ayuda """
    update.message.reply_text('Probá el comando /factoreo para recibir los casos más comunes de factoreo!')


def error(update, context):
    """Loggea los errores causados por el Updater."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Inicia el bot."""
    # Se crea un objeto Updater pasandole el token del bota
    updater = Updater(SECRET_KEY, use_context=True)

    # Obtenemos el dispatcher, del updater, para poder registrar los handlers (métodos)
    disp = updater.dispatcher

    # Para cada comando en telegram se asigna un handler
    disp.add_handler(CommandHandler("start", saludo))
    disp.add_handler(CommandHandler("saludo", saludo))
    disp.add_handler(CommandHandler("ayuda", ayuda))
    disp.add_handler(CommandHandler("factoreo", factoreo))
    
    # loggea todos los errores
    disp.add_error_handler(error)

    # Corre el bot hasta que se presione CTRL+C o el proceso reciba un SIGINT,
    # SIGTERM o SIGABRT.
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=SECRET_KEY)
    updater.bot.setWebhook(
        HEROKU_APP + SECRET_KEY)

    # Dejamos el bot en modo idle para que siga escuchando.
    updater.idle()

if __name__ == '__main__':
    main()
