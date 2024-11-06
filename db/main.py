from db.database import db_session
from db.crud import *


def main():
    db: Session = db_session()

    user = create_user(db, name='Zanny', score=12)
    print(user)


def find_top_users(limit=5):
    db: Session = db_session()

    users = get_users(db)
    users.sort(key=lambda x: -x.score)
    return users[:limit]


def update_score(name, score):
    db: Session = db_session()

    user = get_user_by_name(db, name)
    if not user:
        create_user(db, name, score)
        return

    if score > user.score:
        update_user_score(db, user.id, score)


if __name__ == '__main__':
    for u, e in enumerate(find_top_users()):
        print(u, e.name)
