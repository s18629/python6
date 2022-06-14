from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint
from starlette.responses import Response, JSONResponse
from commands.rooms_commands import update_topic

from database.database import get_database
from rooms import rooms_service
from users.users_service import get_one


class Create(HTTPEndpoint):
    @requires("authenticated")
    async def post(self, request):
        body = await request.json()
        db = get_database()
        rooms_service.create_room(
            db.cursor(), request.user.id, body["password"], body["name"]
        )
        return JSONResponse({})


class Join(HTTPEndpoint):
    @requires("authenticated")
    async def post(self, request):
        body = await request.json()
        db = get_database()
        rooms_service.join_room(
            db.cursor(), request.user.id, request.path_params["id"], body["password"]
        )
        return JSONResponse({})


class ById(HTTPEndpoint):
    @requires("authenticated")
    async def get(self, request):
        db = get_database()

        room = rooms_service.get_room(db.cursor(), request.path_params["id"])
        if rooms_service.joined_room(db, request.user.id, room.id) == False:
            return Response(JSONResponse({}).body, status_code=401)

        topic = rooms_service.get_topic(db.cursor(), room.id)
        users = rooms_service.room_users(db, room.id)
        return JSONResponse(
            {
                "name": room.name,
                "id": room.id,
                "topic": topic.value if topic else "",
                "users": [{"username": user.login} for user in users],
            }
        )

    @requires("authenticated")
    async def patch(self, request):
        body = await request.json()
        db = get_database()
        room_id = request.path_params["id"]
        room = rooms_service.get_room(db, room_id)
        if room is None:
            return Response(JSONResponse({}).body, status_code=401)

        if room.owner_id != request.user.id:
            return Response(JSONResponse({}).body, status_code=401)

        if "topic" in body:
            update_topic(db.cursor(), room_id, body["topic"])

        if "password" in body:
            rooms_service.update_password(db.cursor(), room_id, body["password"])

        users = rooms_service.room_users(db, room.id)
        room_topic = rooms_service.get_topic(db.cursor(), room.id)
        return JSONResponse(
            {
                "name": room.name,
                "id": room.id,
                "topic": room_topic.value if room_topic else "",
                "users": [{"username": user.login} for user in users],
            }
        )


class My(HTTPEndpoint):
    @requires("authenticated")
    async def get(self, request):
        db = get_database()

        rooms = rooms_service.user_rooms(db.cursor(), request.user.id)

        response_rooms = []

        for room in rooms:
            topic = rooms_service.get_topic(db.cursor(), room.id)
            users = rooms_service.room_users(db, room.id)
            owner = get_one(db, room.owner_id)
            response_rooms.append(
                {
                    "name": room.name,
                    "id": room.id,
                    "topic": topic.value if topic else "",
                    "users": [{"username": user.login} for user in users],
                    "owner": owner.login,
                }
            )

        return JSONResponse(response_rooms)


class Vote(HTTPEndpoint):
    @requires("authenticated")
    async def put(self, request):
        body = await request.json()
        db = get_database()
        topic = rooms_service.get_topic(db.cursor(), request.path_params["id"])
        if topic is None:
            return Response(JSONResponse({}).body, status_code=401)

        if not rooms_service.joined_room(db.cursor(), request.user.id, topic.room_id):
            return Response(JSONResponse({}).body, status_code=401)

        rooms_service.add_vote(db.cursor(), topic.id, body["vote"], request.user.id)
        return JSONResponse({})

    @requires("authenticated")
    async def get(self, request):
        db = get_database()
        topic = rooms_service.get_topic(db.cursor(), request.path_params["id"])
        if topic is None:
            return Response(JSONResponse({}).body, status_code=401)

        if not rooms_service.joined_room(db.cursor(), request.user.id, topic.room_id):
            return Response(JSONResponse({}).body, status_code=401)
        votes = []
        for vote in rooms_service.get_votes(db, topic.id):
            user = get_one(db, vote.user_id)
            votes.append({"username": user.login, "value": vote.value})

        return JSONResponse(votes)
