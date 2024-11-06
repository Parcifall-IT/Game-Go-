from sqlalchemy.orm import Session
from db.models import User
from db.database import db_session


def create_user(db: Session, name: str, score: int):
    db_user = User(name=name, score=score)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session):
    return db.query(User).all()


def update_user_score(db: Session, user_id: int, new_score: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.score = new_score
        db.commit()
        db.refresh(user)
    return user


def get_user_by_name(db: Session, user_name: str):
    return db.query(User).filter(User.name == user_name).first()


if __name__ == '__main__':
    db: Session = db_session()
    print(get_user_by_name(db, 'Alex').name)
