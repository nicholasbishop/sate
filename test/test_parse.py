import io
import unittest

from sate.parse import compose, load_satefile, parse_line
from sate.types import Call, Command, Comment, Satefile, Target


class TestParseLine(unittest.TestCase):
    def check(self, src, expected):
        self.assertEqual(list(parse_line(src)), expected)

    def test_command(self):
        self.check('abc', [Command('abc')])

    def test_comment(self):
        self.check('# abc', [Comment(' abc')])

    def test_target(self):
        self.check('[a]', [Target('a')])

    def test_target_with_comment(self):
        self.check('[a] #b', [Target('a'), Comment('b')])

    def test_directive(self):
        self.check('[a] b', [Command(directives=[Call('a')], text='b')])


class TestCompose(unittest.TestCase):
    def check(self, src, expected):
        self.assertEqual(list(compose(src)), expected)

    def test_empty(self):
        self.check([], [])

    def test_empty_target(self):
        self.check([Target('a')], [Target('a')])

    def test_simple_target(self):
        self.check([Target('a'), Command('b')], [Target('a', [Command('b')])])


class TestFullFile(unittest.TestCase):
    def check(self, src, expected):
        rfile = io.StringIO(src)
        self.assertEqual(load_satefile(rfile), expected)

    def test_empty(self):
        self.check('', Satefile())

    # def test_complex(self):
    #     self.check('''
    #     # hello
    #     [a] # world
    #     # hello
    #     b # world

    #     [c deps(a)]
    #     [d] e
    #     ''', Satefile([Target('a', [Command('b')]),
    #                    Target('c', [Command('e', Directive('d'))],
    #                           Directive('deps', ['a']))]))
