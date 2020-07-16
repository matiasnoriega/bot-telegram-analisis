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