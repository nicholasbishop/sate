#!/usr/bin/env python

from __future__ import print_function

import argparse
import logging
import subprocess

LOG = logging.getLogger('sate')


VERSION = '1.1.0'


class Command(object):
    # TODO(nicholasbishop): tags
    def __init__(self, command, tags=None):
        self._command = command
        if tags:
            self._tags = tags.split()

    def append_line(self, line):
        self._command += ' ' + line

    def add_tag(self, tag):
        self._tags.append(tag)

    def run(self, args):
        cmd = ' '.join([self._command] + args)
        print('sate: {}'.format(cmd))
        try:
            subprocess.check_call(cmd, shell=True)
        except subprocess.CalledProcessError as err:
            print('failed: return code {}'.format(err.returncode))
            exit(1)
            # TODO(nicholasbishop): handle failure better


class Target(object):
    def __init__(self, name):
        self._name = name
        self._commands = []

    def __eq__(self, other):
        return (self.name == other.name
                and self.commands == other.commands)

    @property
    def name(self):
        return self._name

    @property
    def commands(self):
        return self._commands

    def add_command(self, line):
        self._commands.append(Command(line))

    def add_command_with_tag(self, tags, line):
        self._commands.append(Command(line, tags))

    def append_line(self, line):
        if not self._commands:
            raise ValueError('no command to append to')
        self._commands[-1].append_line(line)

    def run(self, args):
        for command in self._commands:
            command.run(args)


def parse_tag(line):
    line = line.strip()
    if not line.startswith('['):
        return None, line
    close = line.index(']')
    if close == -1:
        return None, line
    return (line[1:close], line[close + 1:])


def read_stripped_nonempty_lines(rfile):
    for line in rfile.readlines():
        line = line.strip()
        # Skip blank lines
        if line:
            yield line


class SateFile(object):
    def __init__(self, targets=None):
        self._targets = targets or {}

    def __eq__(self, other):
        return self.targets == other.targets

    @property
    def targets(self):
        return self._targets

    @classmethod
    def parse_file(cls, rfile):
        satefile = cls()
        target = None
        for line in read_stripped_nonempty_lines(rfile):
            LOG.debug('line="%s"', line)

            tag, rest = parse_tag(line)
            LOG.debug('tag="%s"', tag)
            LOG.debug('rest="%s"', rest)
            if tag is None:
                target.add_command(rest)
            elif not rest:
                target = Target(tag)
                satefile.add_target(target)
            else:
                target.add_command_with_tag(tag, rest)

            if rest.endswith('\\'):
                # TODO(nicholasbishop): handle continuations
                pass

        return satefile

    def add_target(self, target):
        if target.name in self._targets:
            raise KeyError('target {} already exists'.format(target.name))
        LOG.debug('adding target: %s', target.name)
        self._targets[target.name] = target

    def run_target(self, target, args):
        self._targets[target].run(args)


def list_targets(satefile):
    for name in sorted(satefile.targets):
        print(name)


def parse_command_line():
    parser = argparse.ArgumentParser(description='run tasks')
    parser.add_argument('-f', '--filename', default='.satefile')
    parser.add_argument('-l', '--list', action='store_true')
    parser.add_argument('target', nargs='?')
    parser.add_argument('args', nargs=argparse.REMAINDER)
    return parser.parse_args()


def main():
    logging.basicConfig(level=logging.INFO)
    cl_args = parse_command_line()

    with open(cl_args.filename) as rfile:
        satefile = SateFile.parse_file(rfile)

    if cl_args.list:
        list_targets(satefile)
        return

    # TODO(nicholasbishop): add multiple targets to command line?
    satefile.run_target(cl_args.target, cl_args.args)


if __name__ == '__main__':
    main()
