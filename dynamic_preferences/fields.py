import os
import urlparse
from django.conf import settings
from dynamic_preferences.settings import preferences_settings
from django.db.models.fields.files import FieldFile


class FieldUpfile(FieldFile):

    @property
    def url(self):
        return urlparse.urljoin(settings.MEDIA_URL, os.path.join(preferences_settings.FILE_PREFERENCE_REL_UPLOAD_DIR,
                                                                 self.name))
