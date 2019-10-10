from django.utils.encoding import smart_str

import olduka.v1.authentication.serializers.user_serializers as user_serializers


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': user_serializers.UserSerializer(user, context={'request': request}).data
    }


def get_object_id_value(obj):
    return smart_str(obj._id)
