# service_bot/src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
ENGINEER_TELEGRAM_ID = os.getenv('ENGINEER_TELEGRAM_ID')
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

if not all([TELEGRAM_TOKEN, ENGINEER_TELEGRAM_ID]):
    raise ValueError("Missing required environment variables")