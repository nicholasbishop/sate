import unittest

from sate import types


class TestDeps(unittest.TestCase):
    def test_no_deps(self):
        self.assertEqual(types.Target('a').deps(), [])

    def test_one_dep(self):
        target = types.Target('a', directives=[types.Call('deps', ['b'])])
        self.assertEqual(target.deps(), ['b'])

    def test_two_deps(self):
        target = types.Target('a', directives=[types.Call('deps', ['b', 'c'])])
        self.assertEqual(target.deps(), ['b', 'c'])

    def test_dag(self):
        t_a = types.Target('a', directives=[types.Call('deps', ['b', 'd'])])
        t_b = types.Target('b', directives=[types.Call('deps', ['c', 'd'])])
        t_c = types.Target('c')
        t_d = types.Target('d')
        satefile = types.Satefile((t_a, t_b, t_c, t_d))
        self.assertIn(satefile.deps('a'),
                      (['a', 'b', 'c', 'd'],
                       ['a', 'b', 'd', 'c']))
