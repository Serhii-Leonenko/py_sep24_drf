import pathlib
import uuid

from django.utils.text import slugify


def message_image_file_path(instance, filename):
    filename = (
        f"{slugify(instance.created_at)}-{uuid.uuid4()}" + pathlib.Path(filename).suffix
    )
    return pathlib.Path("messages/images/") / pathlib.Path(filename)
