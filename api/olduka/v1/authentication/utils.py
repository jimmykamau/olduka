def get_jwt_secret(user):
    return user.user_profile.jwt_secret
