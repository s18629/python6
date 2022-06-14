from database.database import Base
from sqlalchemy import Column, Integer, String, Text


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    login = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)

    def __init__(self, login=None, password=None):
        self.login = login
        self.password = password

    # def __init__(self,id, login=None, password=None):
    #     self.id = id
    #     self.login = login
    #     self.password = password

# class User:
#     def __init__(self, id, login=None):
#         self.id = id
#         self.login = login
