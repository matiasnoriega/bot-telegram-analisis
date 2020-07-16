# Modulo dotenv para usar archivo .env
from dotenv import load_dotenv
load_dotenv()

import os
SECRET_KEY = os.getenv("TELEGRAM_BOT_API_KEY")