import argparse

from sate import parse


def find_satefile():
    return '.satefile'


def load_satefile(path):
    with open(path) as rfile:
        return parse.load_satefile(rfile)


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('target', nargs='?')
    parser.add_argument('args', nargs=argparse.REMAINDER)
    args = parser.parse_args()

    satefile = load_satefile(find_satefile())
    satefile.run(args.target, args.args)
