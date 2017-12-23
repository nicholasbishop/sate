from sate import parse

def find_satefile():
    return '.satefile'


def load_satefile(path):
    with open(path) as rfile:
        return list(parse.parse_file(rfile))


def run():
    load_satefile(find_satefile())
