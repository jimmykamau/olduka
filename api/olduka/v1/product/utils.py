from django.utils.encoding import smart_str

def get_object_id_value(obj):
    return smart_str(obj._id)
