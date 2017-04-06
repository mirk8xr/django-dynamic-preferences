from __future__ import unicode_literals
from six import string_types
from django.conf import settings
from django.core.files.storage import default_storage
from django.db.models.fields.files import FieldFile
import os

class SerializationError(Exception):
    pass


class BaseSerializer:
    """
        A serializer take a Python variable and returns a string that can be stored safely in database
    """
    exception = SerializationError

    @classmethod
    def serialize(cls, value, **kwargs):
        """
        Return a string from a Python var
        """
        raise NotImplementedError

    @classmethod
    def deserialize(cls, value, **kwargs):
        """
            Convert a python string to a var
        """
        raise NotImplementedError


class BooleanSerializer(BaseSerializer):
    true = (
        "True",
        "true",
        "TRUE",
        "1",
        "YES",
        "Yes"
        "yes",
    )

    false = (
        "False",
        "false",
        "FALSE",
        "0",
        "No",
        "no"
        "NO"
    )

    @classmethod
    def serialize(cls, value, **kwargs):
        """
            True is serialized to "1" to take less space
            same for False, with "0"
        """
        if value:
            return "1"
        else:
            return "0"

    @classmethod
    def deserialize(cls, value, **kwargs):

        if value in cls.true:
            return True

        elif value in cls.false:
            return False

        else:
            raise cls.exception("Value {0} can't be deserialized to a Boolean".format(value))


class IntSerializer(BaseSerializer):
    @classmethod
    def serialize(cls, value, **kwargs):
        if not isinstance(value, int):
            raise cls.exception('IntSerializer can only serialize int values')

        return value.__str__()

    @classmethod
    def deserialize(cls, value, **kwargs):
        try:
            return int(value)
        except:
            raise cls.exception("Value {0} cannot be converted to int")


from django.template import defaultfilters


class StringSerializer(BaseSerializer):
    @classmethod
    def serialize(cls, value, **kwargs):
        if not isinstance(value, string_types):
            raise cls.exception("Cannot serialize, value {0} is not a string".format(value))

        if kwargs.get("escape_html", False):
            return defaultfilters.force_escape(value)
        else:
            return value

    @classmethod
    def deserialize(cls, value, **kwargs):
        """String deserialisation just return the value as a string"""
        try:
            return str(value)
        except:
            raise cls.exception("Cannot deserialize value {0} tostring".format(value))


DDP_BASE_PATH = ''

class UnsetValue(object):
    pass
UNSET = UnsetValue()

class FileSerializer(BaseSerializer):

    @classmethod
    def serialize(cls, value, **kwargs):
        """
        Return a string from a Python var
        """
        return cls.to_db(value, **kwargs)

    @classmethod
    def deserialize(cls, value, **kwargs):
        """
            Convert a python string to a var
        """
        return cls.to_python(value, **kwargs)

    @classmethod
    def clean_to_db_value(cls, value):
        return value

    @staticmethod
    def handle_uploaded_file(f, path):
        # create folders for upload_to or app dir if necessary
        try:
            os.makedirs(os.path.dirname(path))
        except OSError:
            if not os.path.isdir(os.path.dirname(path)):
                raise

        with open(path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

    @classmethod
    def to_db(cls, file, **kwargs):
        # to_db is passed a file object from forms.FileField
        if not settings.MEDIA_ROOT:
            raise cls.exception("You need to set MEDIA_ROOT in your settings.py")

        try:
            path = os.path.join(settings.MEDIA_ROOT, DDP_BASE_PATH, file.name)
            cls.handle_uploaded_file(file, path)
            # TODO: delete previous file (if any)
        except AttributeError:
            return ''

        return file.name

    @classmethod
    def to_python(cls, value, **kwargs):
        filename = value
        if not settings.MEDIA_ROOT:
            raise cls.exception("You need to set MEDIA_ROOT in your settings.py")

        path = os.path.join(settings.MEDIA_ROOT, DDP_BASE_PATH, filename)

        if os.path.isfile(path):
            # https://yuji.wordpress.com/2013/01/30/django-form-field-in-initial-data-requires-a-fieldfile-instance/
            # TODO: Understand this FieldFile better and maybe remove the FakeField workaround
            class FakeField(object):
                storage = default_storage

            fieldfile = FieldFile(None, FakeField, path)
            return fieldfile
        else:
            return None
