from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import DATABASE_URL
#export DATABASE_URL="mysql+mysqlconnector://bot:qwer1234t5@localhost:3308/bot_db"


database = Database(DATABASE_URL)
engine = create_engine(
    DATABASE_URL,echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


