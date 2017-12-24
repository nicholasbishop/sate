import collections
import copy
import subprocess

import attr
import dag


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

    def deps(self):
        for directive in self.directives:
            if directive.name == 'deps':
                return directive.args
        return []

    def run(self, args):
        for command in self.commands:
            command.run(args)


def target_list_to_dict(lst):
    lst = lst or []
    dct = collections.OrderedDict()
    for target in lst:
        if target.name in dct:
            raise KeyError('duplicate target name: ' + target.name)
        dct[target.name] = target
    return dct


@attr.s(frozen=True, slots=True)
class Satefile(object):
    targets = attr.ib(
        default=attr.Factory(collections.OrderedDict),
        validator=attr.validators.instance_of(collections.abc.Mapping),
        convert=target_list_to_dict)

    def run(self, target_name, args):
        if target_name not in self.targets:
            exit('error: unknown target')
        for dep in reversed(self.deps(target_name)):
            self.targets[dep].run(args)
        self.targets[target_name].run(args)

    def deps(self, original_target):
        graph = dag.DAG()

        remaining = [original_target]
        while remaining:
            target = remaining.pop()
            graph.add_node_if_not_exists(target)
            deps = self.targets[target].deps()
            for dep in deps:
                graph.add_node_if_not_exists(dep)
                graph.add_edge(target, dep)
            remaining += deps

        return graph.all_downstreams(original_target)
