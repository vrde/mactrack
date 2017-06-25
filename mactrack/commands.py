import argparse

from . import config
config.setup_logging()

import logging
log = logging.getLogger(__name__)


def emit(args):
    from . import emit
    emit.run()


def main():
    log.info('Starting mactrack')
    config.setup_database()
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    emit(args)


if __name__ == '__main__':
    main()
