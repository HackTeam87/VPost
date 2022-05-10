from starlette.config import Config
config = Config(".env")
# Переменная окружения
DATABASE_URL = config("DATABASE_URL", cast=str, default="")
#export DATABASE_URL="mysql+mysqlconnector://user:passwd@localhost:3308/bot_db"
TELEGRAM_TOCKEN = config("TELEGRAM_TOCKEN", cast=str, default="")
#export TELEGRAM_TOCKEN=""


