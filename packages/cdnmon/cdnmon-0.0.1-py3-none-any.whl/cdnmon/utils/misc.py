import datetime
import os
from pathlib import Path


def get_project_root():
    return Path(__file__).parent.parent.parent


def get_filename_no_ext(filepath):
    filename, ext = os.path.splitext(os.path.basename(filepath))
    return filename


def get_module_name(m):
    return m.__name__.split(".")[-1]


def yesterday():
    return datetime.datetime.today() - datetime.timedelta(days=1)
