import os
import sqlite3

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


db_path = os.path.join(os.path.dirname(os.path.abspath(__name__)), "db.sqlite")

db = None



DATABASE_NAME = 'db.sqlite'
engine = create_engine(f'sqlite:///{DATABASE_NAME}')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


def create_db():
    Base.metadata.create_all(engine)
    print('tables has been created sucessfully')


def get_database() -> sqlite3.Connection:
    global db
    if db is None:
        db = sqlite3.connect(db_path)
        db.execute("PRAGMA foreign_keys = ON;")
    return db


def initialize(db: sqlite3.Connection):
    print("Dropping db")
    db.isolation_level = None
    for call in [
        "PRAGMA writable_schema = 1;",
        "DELETE FROM sqlite_master;",
        "PRAGMA writable_schema = 0;",
        "VACUUM;",
        "PRAGMA integrity_check;",
    ]:
        db.execute(call)

    db.isolation_level = ""
    cursor = db.cursor()
    cursor.execute(
        """
    CREATE TABLE users (
        id integer PRIMARY KEY,
        login text NOT NULL UNIQUE,
        password text NOT NULL
    )
    """
    )

    cursor.execute(
        """
        CREATE TABLE rooms (
            id integer PRIMARY KEY,
            name text NOT NULL,
            password text NOT NULL,
            owner_id integer NOT NULL,
            FOREIGN KEY (owner_id) REFERENCES users (id) 
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE joined_rooms (
            id integer PRIMARY KEY,
            room_id integer NOT NULL,
            user_id integer NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ,
            FOREIGN KEY (room_id) REFERENCES rooms (id) ,
            UNIQUE(room_id, user_id)
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE topics (
            id integer PRIMARY KEY,
            room_id integer NOT NULL UNIQUE,
            value text NOT NULL,
            FOREIGN KEY (room_id) REFERENCES rooms (id)
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE votes (
            id integer PRIMARY KEY,
            topic_id integer NOT NULL,
            user_id integer NOT NULL,
            value float NOT NULL,
            FOREIGN KEY (topic_id) REFERENCES topics (id),
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE (user_id, topic_id)
        )
    """
    )
