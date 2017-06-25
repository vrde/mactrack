import argparse


def emit(args):
    from . import emit
    emit.run()


def main():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    emit(args)


if __name__ == '__main__':
    main()
