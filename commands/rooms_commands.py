from database.users_model import User
from rooms import rooms_service
from sqlite3 import Cursor


def update_topic(db: Cursor, room_id: int, new_topic: str):
    topic = rooms_service.get_topic(db, room_id)
    if topic is not None:
        rooms_service.remove_all_votes(db, topic.id)
        rooms_service.remove_topic(db, room_id)

    rooms_service.create_topic(db, room_id, new_topic)
