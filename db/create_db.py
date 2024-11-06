from database import engine
from models import Base


def create_tables():
    Base.metadata.create_all(engine)
    print("Таблицы успешно созданы")
    print(Base.metadata.tables)


if __name__ == "__main__":
    create_tables()
