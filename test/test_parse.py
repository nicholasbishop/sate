import logging
import unittest

from sate.parse import Command, Comment, Target, compose, parse_line

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
        self.check('[a] b', [Command(directives='a', text='b')])


class TestCompose(unittest.TestCase):
    def check(self, src, expected):
        self.assertEqual(list(compose(src)), expected)

    def test_empty(self):
        self.check([], [])

    def test_empty_target(self):
        self.check([Target('a')], [Target('a')])

    def test_simple_target(self):
        self.check([Target('a'), Command('b')],
                   [Target('a', [Command('b')])])


logging.basicConfig(level=logging.DEBUG)
