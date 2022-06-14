from database.database import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    owner_id = Column(Integer, nullable=False)
    password = Column(Text, nullable=False)
    name = Column(Text, nullable=False)


    def __init__(self, id: int, owner_id: int, password: str, name: str):
        self.id = id
        self.owner_id = owner_id
        self.password = password
        self.name = name


# class Room:
#     def __init__(self, id: int, owner_id: int, password: str, name: str):
#         self.id = id
#         self.owner_id = owner_id
#         self.password = password
#         self.name = name


class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    room_id = Column(Integer, nullable=False)
    value = Column(String)

    def __init__(self, id: int, room_id: int, value: str):
        self.id = id
        self.room_id = room_id
        self.value = value


# class Topic:
#     def __init__(self, id: int, room_id: int, value: str):
#         self.id = id
#         self.room_id = room_id
#         self.value = value


class Vote(Base):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    topic_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    value = Column(String)

    def __init__(self, id: int, topic_id: int, user_id: int, value: str):
        self.id = id
        self.topic_id = topic_id
        self.user_id = user_id
        self.value = value


# class Vote:
#     def __init__(self, id: int, topic_id: int, user_id: int, value: str):
#         self.id = id
#         self.topic_id = topic_id
#         self.user_id = user_id
#         self.value = value
