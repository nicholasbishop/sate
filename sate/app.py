import argparse

from sate import VERSION, parse


def find_satefile():
    return '.satefile'


def load_satefile(path):
    with open(path) as rfile:
        return parse.load_satefile(rfile)


def print_targets(satefile):
    for target in satefile.targets:
        print(target)


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-l', '--list', help='list targets', action='store_true')
    parser.add_argument('--version', action='store_true')
    parser.add_argument('target', nargs='?')
    parser.add_argument('args', nargs=argparse.REMAINDER)
    args = parser.parse_args()

    satefile = load_satefile(find_satefile())

    if args.version:
        print(VERSION)
    elif args.list:
        print_targets(satefile)
    else:
        satefile.run(args.target, args.args)
