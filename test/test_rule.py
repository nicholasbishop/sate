import unittest

from sate import rules, types


class TestCall(unittest.TestCase):
    def test_one_char(self):
        self.assertEqual(rules.Call.parse('a()'), types.Call('a'))

    def test_two_char(self):
        self.assertEqual(rules.Call.parse('ab()'), types.Call('ab'))

    def test_no_parens(self):
        self.assertEqual(rules.Call.parse('a'), types.Call('a'))

    def test_two_char_no_parens(self):
        self.assertEqual(rules.Call.parse('ab'), types.Call('ab'))

    def test_args(self):
        self.assertEqual(
            rules.Call.parse('a(b c d)'), types.Call('a', ['b', 'c', 'd']))


class TestCommandTag(unittest.TestCase):
    def test_one_char(self):
        self.assertEqual(rules.CommandTag.parse('[a]'), [types.Call('a')])

    def test_two_char(self):
        self.assertEqual(rules.CommandTag.parse('[ab]'), [types.Call('ab')])

    def test_call(self):
        self.assertEqual(rules.CommandTag.parse('[a()]'), [types.Call('a')])


class TestTargetTag(unittest.TestCase):
    def test_one_char(self):
        self.assertEqual(rules.TargetTag.parse('[a]'), types.Target('a'))

    def test_two_char(self):
        self.assertEqual(rules.TargetTag.parse('[ab]'), types.Target('ab'))

    def test_no_args(self):
        self.assertEqual(
            rules.TargetTag.parse('[a b]'),
            types.Target('a', directives=[types.Call('b')]))
