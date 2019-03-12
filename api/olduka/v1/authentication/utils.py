import uuid


def get_jwt_secret(user):
    return user.user_profile.jwt_secret


def change_jwt_secret(user):
    user.user_profile.jwt_secret = uuid.uuid4()
    user.user_profile.save()
