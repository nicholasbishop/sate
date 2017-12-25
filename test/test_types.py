import unittest

from sate import types


class TestSeparateDeps(unittest.TestCase):
    def check(self, src, expected):
        self.assertEqual(types.separate_deps_from_directives(src), expected)

    def test_empty(self):
        self.check([], ([], []))

    def test_just_deps(self):
        self.check([types.Call('deps', ['a'])], (['a'], []))

    def test_both(self):
        self.check([types.Call('deps', ['a']), types.Call('b')],
                   (['a'], [types.Call('b')]))


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
        self.assertEqual(satefile.deps('a'), ['b', 'c', 'd'])

    def test_four_targets(self):
        satefile = types.Satefile([
            types.Target('lint'),
            types.Target('format'),
            types.Target('test'),
            types.Target('sanity').with_deps('format', 'lint', 'test')])
        self.assertEqual(satefile.deps('sanity'), ['format', 'lint', 'test'])
