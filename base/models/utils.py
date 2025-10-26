import os
from django.utils.crypto import get_random_string

def create_id():
    return get_random_string(22)


def upload_image_to(instance, filename):
    item_id = str(instance.id)
    return os.path.join('static', 'items', item_id, filename)