from database.users_model import User
from users import users_service




class RegisterException(Exception):
    pass


class WrongDataException(RegisterException):
    pass


class UserExistsException(RegisterException):
    pass


# def register(db, login, password):
#     if not users_service.validate_login(login):
#         raise WrongDataException("Wrong login")
#
#     if not users_service.validate_password(password):
#         raise WrongDataException("Wrong password")
#
#     if users_service.has_user(db, login):
#         raise UserExistsException("User exists")
#
#     with db:
#         users_service.create_user(db, login, password)


def register(login, password):
    if not users_service.validate_login(login):
        raise WrongDataException("Wrong login")

    if not users_service.validate_password(password):
        raise WrongDataException("Wrong password")

    # if users_service.has_user(login):
    #     raise UserExistsException("User exists")

    users_service.create_user(login, password)


def login(db, login, password) -> User:
    return users_service.login(db, login, password)