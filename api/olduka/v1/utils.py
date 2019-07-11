import olduka.v1.authentication.serializers.user_serializers as user_serializers


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': user_serializers.UserSerializer(user, context={'request': request}).data
    }
