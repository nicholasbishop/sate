import collections
import subprocess

import attr


@attr.s(frozen=True, slots=True)
class Call(object):
    name = attr.ib(validator=attr.validators.instance_of(str))
    args = attr.ib(default=attr.Factory(list))


@attr.s(frozen=True, slots=True)
class Command(object):
    text = attr.ib()
    directives = attr.ib(default=attr.Factory(list))

    def with_directives(self, directives):
        return Command(text=self.text, directives=directives)

    def run(self, extra_args):
        cmd = ' '.join([self.text] + extra_args)
        print(cmd)
        try:
            subprocess.check_call(cmd, shell=True)
        except subprocess.CalledProcessError as err:
            print('failed with exit code {}'.format(err.returncode))


@attr.s(frozen=True, slots=True)
class Comment(object):
    text = attr.ib()


@attr.s(frozen=True, slots=True)
class Target(object):
    name = attr.ib()
    commands = attr.ib(default=attr.Factory(list))
    directives = attr.ib(default=attr.Factory(list))

    def add_command(self, command):
        return Target(name=self.name, commands=self.commands + [command])

    def run(self, args):
        for command in self.commands:
            command.run(args)


@attr.s
class Satefile(object):
    targets = attr.ib(default=attr.Factory(collections.OrderedDict))

    def run(self, target_name, args):
        if target_name not in self.targets:
            exit('error: unknown target')
        self.targets[target_name].run(args)
