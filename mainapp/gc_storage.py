from __future__ import absolute_import
import datetime
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest
from django.core.files.storage import FileSystemStorage
import os


def _check_extension(filename, allowed_extensions):
    if ('.' not in filename or
            filename.split('.').pop().lower() not in allowed_extensions):
        raise BadRequest(
            "{0} has an invalid name or extension".format(filename))


def _safe_filename(filename):
    """
    Generates a safe filename that is unlikely to collide with existing objects
    in Google Cloud Storage.
    ``filename.ext`` is transformed into ``filename-YYYY-MM-DD-HHMMSS.ext``
    """
    filename = secure_filename(filename)
    date = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
    basename, extension = filename.rsplit('.', 1)
    return "{0}-{1}.{2}".format(basename, date, extension)


def save_file(myfile, name=None):
    if name:
        filename = _safe_filename(name)
    else:
        filename = _safe_filename(myfile.name)
        fs = FileSystemStorage(location='uploads')  # defaults to   MEDIA_ROOT
    filename = fs.save(filename, myfile)
    file_url = fs.url(filename)
    return file_url

