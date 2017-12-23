import io
import logging
import unittest

from sate.parse import compose, load_satefile, parse_directives, parse_line
from sate.types import Command, Comment, Directive, Satefile, Target


class TestParseDirectives(unittest.TestCase):
    def check(self, src, expected):
        self.assertEqual(list(parse_directives(src)), expected)

    def test_simple(self):
        self.check('a', [Directive('a')])

    def test_one_dep(self):
        self.check('deps(a)', [Directive('deps', ['a'])])

    def test_two_deps(self):
        self.check('deps(a b)', [Directive('deps', ['a', 'b'])])

    def test_two_directives(self):
        self.check('a b', [Directive('a'), Directive('b')])


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
        self.check('[a] b', [Command(directives=[Directive('a')], text='b')])


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
        rfile = io.StringIO(unicode(src))
        self.assertEqual(load_satefile(rfile), expected)

    def test_empty(self):
        self.check('', Satefile())


logging.basicConfig(level=logging.DEBUG)
