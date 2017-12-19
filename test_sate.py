#!/usr/bin/env python

from __future__ import unicode_literals

import io
import unittest

import sate


class TestSate(unittest.TestCase):
    def _check_read_lines(self, text, expected):
        rfile = io.StringIO(text)
        lines = sate.read_stripped_nonempty_lines(rfile)
        self.assertEqual(list(lines), expected)

    def _check_parse(self, text, expected):
        rfile = io.StringIO(text)
        self.assertEqual(sate.SateFile().parse_file(rfile),
                         sate.SateFile(expected))

    def test_read_lines(self):
        self._check_read_lines('a', ['a'])

    def test_read_lines_empty(self):
        self._check_read_lines('\n', [])

    def test_read_lines_trim(self):
        self._check_read_lines('a\n', ['a'])

    def test_parse_target(self):
        self._check_parse('[a]', {'a': sate.Target('a')})

    def test_parse_variable(self):
        sat = sate.SateFile.parse('[var="a"]')
        self.assertEqual(sat.variables, {'var': 'a'})


if __name__ == '__main__':
    unittest.main()
