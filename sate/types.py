import collections
import copy
import subprocess

import attr
import toposort

DEPS_KEY = 'deps'


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


def separate_deps_from_directives(original_directives):
    directives = []
    deps = []
    for directive in original_directives:
        if directive.name == DEPS_KEY:
            deps += directive.args
        else:
            directives.append(directive)
    return deps, directives


@attr.s(frozen=True, slots=True)
class Target(object):
    name = attr.ib()
    commands = attr.ib(default=attr.Factory(list))
    directives = attr.ib(default=attr.Factory(list))

    def add_command(self, command):
        return Target(name=self.name, commands=self.commands + [command])

    def deps(self):
        for directive in self.directives:
            if directive.name == DEPS_KEY:
                return directive.args
        return []

    def run(self, args):
        for command in self.commands:
            command.run(args)

    def with_deps(self, *new_deps):
        deps, directives = separate_deps_from_directives(self.directives)
        commands = copy.copy(self.commands)
        for dep in new_deps:
            if dep not in deps:
                deps.append(dep)
        directives.append(Call(DEPS_KEY, deps))
        return Target(name=self.name, commands=commands, directives=directives)


def target_list_to_dict(lst):
    lst = lst or []
    dct = collections.OrderedDict()
    for target in lst:
        if target.name in dct:
            raise KeyError('duplicate target name: ' + target.name)
        dct[target.name] = target
    return dct


def make_target_graph(all_targets, original_target):
    graph = {}

    def init_node(target):
        if target not in graph:
            graph[target] = set()

    stack = [original_target]
    while stack:
        target = stack.pop()
        init_node(target)
        deps = all_targets[target].deps()
        for dep in deps:
            init_node(dep)
            graph[target].add(dep)
        stack += deps

    return graph


@attr.s(frozen=True, slots=True)
class Satefile(object):
    targets = attr.ib(
        default=attr.Factory(collections.OrderedDict),
        validator=attr.validators.instance_of(collections.abc.Mapping),
        convert=target_list_to_dict)

    def run(self, target_name, args):
        if target_name not in self.targets:
            exit('error: unknown target')
        for dep in reversed(self.run_order(target_name)):
            self.targets[dep].run(args)

    def run_order(self, target):
        graph = make_target_graph(self.targets, target)
        return list(toposort.toposort_flatten(graph))
