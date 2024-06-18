from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

ENGINE = create_engine('postgresql://postgres:3110@localhost/shopping_furniture', echo=True)
Base = declarative_base()
session = sessionmaker()
