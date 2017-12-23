import subprocess

import attr


@attr.s(frozen=True, slots=True)
class Command(object):
    text = attr.ib()
    directives = attr.ib(default=attr.Factory(list))

    def with_directives(self, directives):
        return Command(text=self.text, directives=directives)

    def run(self, extra_args):
        cmd = ' '.join([self.text] + extra_args)
        print(cmd)
        subprocess.check_call(cmd, shell=True)


@attr.s(frozen=True, slots=True)
class Comment(object):
    text = attr.ib()


@attr.s(frozen=True, slots=True)
class Target(object):
    name = attr.ib()
    commands = attr.ib(default=attr.Factory(list))

    def add_command(self, command):
        return Target(name=self.name, commands=self.commands + [command])

    def run(self, args):
        for command in self.commands:
            command.run(args)


@attr.s
class Satefile(object):
    targets = attr.ib()

    def run(self, target_name, args):
        self.targets[target_name].run(args)
