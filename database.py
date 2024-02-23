from pathlib import Path
import os
from dotenv import load_dotenv
import psycopg2


# Подключение файла .env
BASE_DIR = Path(__file__).resolve().parent
dot_env = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path=dot_env)


def connect():
    """Создание соединения с базой"""

    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST")
    )
    return conn
