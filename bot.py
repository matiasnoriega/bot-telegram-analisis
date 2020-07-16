import os
import re
import requests

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
URL_API_LATEX2PNG = 'http://latex2png.com/api/convert'
URL_BASE_LATEX2PNG = 'http://latex2png.com'

# Definimos algunos comandos básicos que funcionaran como handlers.

def saludo(update, context):
    """Manda un mensaje cuando el usuario ingresa /saludo """
    update.message.reply_text('Hola! Soy el BOT de Análisis Matemático! Sirvo como un ayuda-memoria para la cursada')

def factoreo(update, context):
    """ Devuelve tabla de casos mas comunes de factoreo """
    update.message.reply_photo(photo=open('assets/factoreo.png', 'rb'))

def ayuda(update, context):
    """Manda un mensaje cuando el usuario ingresa /ayuda """
    update.message.reply_text('Probá el comando /factoreo para recibir los casos más comunes de factoreo o /derivar funcion para ver la derivada de f(x)!')

def derivar(update, context):
    """ Toma la función base y muestra su derivada """
    #se declara un diccionario de patrones para contrastar la funcion recibida
    patron_funciones = {
        '^[0-9]+$': '0',
        'x$': '1',
        '': '',
    }

    #Tomamos el primer argumento que se le pasa al comando como función f(x)
    funcion = context.args[0]
    resultado = None

    for key in patron_funciones.keys():
        #compilamos el patron de esta entrada particular del diccionario para compararlo con la funcion recibida
        #y guardamos el resultado en la variable match
        regex_matcher = re.compile(key)
        match = regex_matcher.match(funcion)
        #si hubo una coincidencia, guardamos en la variable resultado el valor asociado a esa clave en el diccionario
        #devolvemos resultado y detenemos el ciclo for
        if match:
            resultado = patron_funciones.get(key)
            break

    # Si encuentra una coincidencia usa la API de Latex2PNG
    if(resultado):

        # Data para mandar a la API de latex2png
        payload = "{\n\"auth\": {\n\"user\": \"guest\",\n\"password\": \"guest\"\n},\n\"latex\": \"%(latex)s\" ,\n\"resolution\": 600,\n\"color\": \"111111\"\n}"%{'latex': resultado}
        # Headers del Request
        headers = {
            'Content-Type': 'application/json'
        }

        r = requests.request("POST", 'http://latex2png.com/api/convert', headers=headers, data=payload)
        
        json_response = r.json()
        img_url = json_response["url"]
        update.message.reply_photo('http://latex2png.com' + img_url)

    else:
        update.message.reply_text('No encontré una función base que coincida con '+ context.args[0])

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
    disp.add_handler(CommandHandler("derivar", derivar, pass_args=True))
    
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
