import os
import logging

import coloredlogs

from . import db


def setup_logging(level=logging.DEBUG):
    coloredlogs.install(level=level)


def setup_database():
    if not os.path.exists(db.FILENAME):
        db.create_tables()
