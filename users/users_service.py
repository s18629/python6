import re
from sqlite3 import Cursor
from typing import List

import bcrypt

from database.database import Base
from sqlalchemy.orm import sessionmaker
from database.database import engine, session, sessionmaker

from database.users_model import User

LOGIN_RE = r"^[a-zA-Z0-9]+$"


def validate_login(login: str):
    if not len(login) > 3:
        return False

    return re.match(LOGIN_RE, login) is not None


def validate_password(password):
    return len(password) > 4


def has_user(db: Cursor, login: str):
    return (
            len(db.execute("SELECT * FROM users WHERE login = ?", (login,)).fetchall()) > 0
    )


def login(db: Cursor, login: str, password: str):
    user = db.execute("SELECT * FROM users WHERE login = ?", (login,)).fetchone()
    if user is None:
        return None

    if not bcrypt.checkpw(password.encode("utf-8"), user[2].encode("utf-8")):
        return None

    return User(id=user[0], login=user[1])


def create_user(login: str, password):
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    # db.execute(
    #     "INSERT INTO users (login, password) VALUES (?, ?)", (login.lower(), password)
    # )

    user = User(
        login=login,
        password=password
    )
    session.add(user)
    session.commit()




# def create_user(db: Cursor, login: str, password):
#     salt = bcrypt.gensalt()
#     password = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
#
# db.execute(
#     "INSERT INTO users (login, password) VALUES (?, ?)", (login.lower(), password)
# )
#


def get_all_users(db: Cursor) -> List[User]:
    return [
        User(id=user[0], login=user[1]) for user in db.execute("SELECT * FROM users")
    ]


def get_one(db: Cursor, id: int) -> User:
    user = db.execute("SELECT * FROM users WHERE id = ?", (id,)).fetchone()
    return User(id=user[0], login=user[1])


def remove_user(db: Cursor, login):
    db.execute("DELETE FROM users WHERE login = ?", (login,))
