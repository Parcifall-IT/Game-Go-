from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

DATABASE_URL = 'postgresql://operator:operator@localhost:5432/godb'

engine = create_engine(DATABASE_URL, echo=True)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()


if __name__ == '__main__':
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            for row in result:
                print(f"PostgreSQL version: {row[0]}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")
