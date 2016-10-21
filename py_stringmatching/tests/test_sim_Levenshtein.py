# coding=utf-8

from __future__ import unicode_literals

import math
import unittest

from nose.tools import *

from py_stringmatching.similarity_measure.levenshtein import Levenshtein

class LevenshteinTestCases(unittest.TestCase):
    def setUp(self):
        self.lev = Levenshtein()

    def test_valid_input_raw_score(self):
        # http://oldfashionedsoftware.com/tag/levenshtein-distance/
        self.assertEqual(self.lev.get_raw_score('a', ''), 1)
        self.assertEqual(self.lev.get_raw_score('', 'a'), 1)
        self.assertEqual(self.lev.get_raw_score('abc', ''), 3)
        self.assertEqual(self.lev.get_raw_score('', 'abc'), 3)
        self.assertEqual(self.lev.get_raw_score('', ''), 0)
        self.assertEqual(self.lev.get_raw_score('a', 'a'), 0)
        self.assertEqual(self.lev.get_raw_score('abc', 'abc'), 0)
        self.assertEqual(self.lev.get_raw_score('a', 'ab'), 1)
        self.assertEqual(self.lev.get_raw_score('b', 'ab'), 1)
        self.assertEqual(self.lev.get_raw_score('ac', 'abc'), 1)
        self.assertEqual(self.lev.get_raw_score('abcdefg', 'xabxcdxxefxgx'), 6)
        self.assertEqual(self.lev.get_raw_score('ab', 'a'), 1)
        self.assertEqual(self.lev.get_raw_score('ab', 'b'), 1)
        self.assertEqual(self.lev.get_raw_score('abc', 'ac'), 1)
        self.assertEqual(self.lev.get_raw_score('xabxcdxxefxgx', 'abcdefg'), 6)
        self.assertEqual(self.lev.get_raw_score('a', 'b'), 1)
        self.assertEqual(self.lev.get_raw_score('ab', 'ac'), 1)
        self.assertEqual(self.lev.get_raw_score('ac', 'bc'), 1)
        self.assertEqual(self.lev.get_raw_score('abc', 'axc'), 1)
        self.assertEqual(self.lev.get_raw_score('xabxcdxxefxgx', '1ab2cd34ef5g6'), 6)
        self.assertEqual(self.lev.get_raw_score('example', 'samples'), 3)
        self.assertEqual(self.lev.get_raw_score('sturgeon', 'urgently'), 6)
        self.assertEqual(self.lev.get_raw_score('levenshtein', 'frankenstein'), 6)
        self.assertEqual(self.lev.get_raw_score('distance', 'difference'), 5)
        self.assertEqual(self.lev.get_raw_score('java was neat', 'scala is great'), 7)

    def test_valid_input_sim_score(self):
        self.assertEqual(self.lev.get_sim_score('a', ''), 1.0 - (1.0/1.0))
        self.assertEqual(self.lev.get_sim_score('', 'a'), 1.0 - (1.0/1.0))
        self.assertEqual(self.lev.get_sim_score('abc', ''), 1.0 - (3.0/3.0))
        self.assertEqual(self.lev.get_sim_score('', 'abc'), 1.0 - (3.0/3.0))
        self.assertEqual(self.lev.get_sim_score('', ''), 1.0)
        self.assertEqual(self.lev.get_sim_score('a', 'a'), 1.0)
        self.assertEqual(self.lev.get_sim_score('abc', 'abc'), 1.0)
        self.assertEqual(self.lev.get_sim_score('a', 'ab'), 1.0 - (1.0/2.0))
        self.assertEqual(self.lev.get_sim_score('b', 'ab'), 1.0 - (1.0/2.0))
        self.assertEqual(self.lev.get_sim_score('ac', 'abc'), 1.0 - (1.0/3.0))
        self.assertEqual(self.lev.get_sim_score('abcdefg', 'xabxcdxxefxgx'), 1.0 - (6.0/13.0))
        self.assertEqual(self.lev.get_sim_score('ab', 'a'), 1.0 - (1.0/2.0))
        self.assertEqual(self.lev.get_sim_score('ab', 'b'), 1.0 - (1.0/2.0))
        self.assertEqual(self.lev.get_sim_score('abc', 'ac'), 1.0 - (1.0/3.0))
        self.assertEqual(self.lev.get_sim_score('xabxcdxxefxgx', 'abcdefg'), 1.0 - (6.0/13.0))
        self.assertEqual(self.lev.get_sim_score('a', 'b'), 1.0 - (1.0/1.0))
        self.assertEqual(self.lev.get_sim_score('ab', 'ac'), 1.0 - (1.0/2.0))
        self.assertEqual(self.lev.get_sim_score('ac', 'bc'), 1.0 - (1.0/2.0))
        self.assertEqual(self.lev.get_sim_score('abc', 'axc'), 1.0 - (1.0/3.0))
        self.assertEqual(self.lev.get_sim_score('xabxcdxxefxgx', '1ab2cd34ef5g6'), 1.0 - (6.0/13.0))
        self.assertEqual(self.lev.get_sim_score('example', 'samples'), 1.0 - (3.0/7.0))
        self.assertEqual(self.lev.get_sim_score('sturgeon', 'urgently'), 1.0 - (6.0/8.0))
        self.assertEqual(self.lev.get_sim_score('levenshtein', 'frankenstein'), 1.0 - (6.0/12.0))
        self.assertEqual(self.lev.get_sim_score('distance', 'difference'), 1.0 - (5.0/10.0))
        self.assertEqual(self.lev.get_sim_score('java was neat', 'scala is great'), 1.0 - (7.0/14.0))

    def test_valid_input_non_ascii_raw_score(self):
        self.assertEqual(self.lev.get_raw_score('ác', 'áóc'), 1)
        self.assertEqual(self.lev.get_raw_score(u'ác', u'áóc'), 1)
        self.assertEqual(self.lev.get_raw_score(b'\xc3\xa1c', b'\xc3\xa1\xc3\xb3c'), 1)

    def test_valid_input_non_ascii_sim_score(self):
        self.assertEqual(self.lev.get_sim_score('ác', 'áóc'), 1.0 - (1.0/3.0))
        self.assertEqual(self.lev.get_sim_score(u'ác', u'áóc'), 1.0 - (1.0/3.0))
        self.assertEqual(self.lev.get_sim_score(b'\xc3\xa1c', b'\xc3\xa1\xc3\xb3c'), 1.0 - (1.0/3.0))

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.lev.get_raw_score('a', None)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.lev.get_raw_score(None, 'b')

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.lev.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.lev.get_raw_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.lev.get_raw_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.lev.get_raw_score(12.90, 12.90)

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.lev.get_sim_score('a', None)

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.lev.get_sim_score(None, 'b')

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.lev.get_sim_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_sim_score(self):
        self.lev.get_sim_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_sim_score(self):
        self.lev.get_sim_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_sim_score(self):
        self.lev.get_sim_score(12.90, 12.90)