from pathlib import Path

from django.core.files import File


def get_file_name(filename):
    return filename.split(".")[0]


def get_extension(filename):
    return filename.split(".")[-1].lower()


def get_or_create_file_object(Model, path: Path, filename):
    try:
        if not (obj := Model.objects.filter(title=filename).first()):
            with open(path / filename, "rb") as f:
                obj = Model.objects.create(title=filename, file=File(f, name=filename))
        return obj
    except: ...
