import unittest

from sate import rules, types

class TestCall(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(rules.Call.parse('a()'), ['a', []])

    def test_args(self):
        self.assertEqual(rules.Call.parse('a(b c d)'),
                         ['a', ['b', 'c', 'd']])


class TestCommandTag(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(rules.CommandTag.parse('[a]'),
                         [types.Directive('a')])

    def test_call(self):
        self.assertEqual(rules.CommandTag.parse('[a()]'),
                         [types.Directive('a')])


class TestTargetTag(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(rules.TargetTag.parse('[a]'),
                         types.Target('a'))

    def test_no_args(self):
        self.assertEqual(rules.TargetTag.parse('[a b]'),
                         types.Target('a', directives=[types.Directive('b')]))
