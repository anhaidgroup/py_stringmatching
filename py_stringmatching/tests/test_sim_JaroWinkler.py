# coding=utf-8

from __future__ import unicode_literals

import math
import unittest

from nose.tools import *

from py_stringmatching.similarity_measure.jaro_winkler import JaroWinkler

class JaroWinklerTestCases(unittest.TestCase):
    def setUp(self):
        self.jw = JaroWinkler()

    def test_get_prefix_weight(self):
        self.assertEqual(self.jw.get_prefix_weight(), 0.1)

    def test_set_prefix_weight(self):
        jw = JaroWinkler(prefix_weight=0.15)
        self.assertEqual(jw.get_prefix_weight(), 0.15)
        self.assertAlmostEqual(jw.get_raw_score('MARTHA', 'MARHTA'), 0.9694444444444444)
        self.assertEqual(jw.set_prefix_weight(0.25), True)
        self.assertEqual(jw.get_prefix_weight(), 0.25)
        self.assertAlmostEqual(jw.get_raw_score('MARTHA', 'MARHTA'), 0.9861111111111112)

    def test_valid_input_raw_score(self):
        # https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance
        self.assertAlmostEqual(self.jw.get_raw_score('MARTHA', 'MARHTA'),
                               0.9611111111111111)
        self.assertAlmostEqual(self.jw.get_raw_score('DWAYNE', 'DUANE'), 0.84)
        self.assertAlmostEqual(self.jw.get_raw_score('DIXON', 'DICKSONX'),
                               0.8133333333333332)

    def test_valid_input_sim_score(self):
        self.assertAlmostEqual(self.jw.get_sim_score('MARTHA', 'MARHTA'),
                               0.9611111111111111)
        self.assertAlmostEqual(self.jw.get_sim_score('DWAYNE', 'DUANE'), 0.84)
        self.assertAlmostEqual(self.jw.get_sim_score('DIXON', 'DICKSONX'),
                               0.8133333333333332)

    def test_non_ascii_input_raw_score(self):
        self.assertAlmostEqual(self.jw.get_raw_score(u'MARTHA', u'MARHTA'),
                               0.9611111111111111)
        self.assertAlmostEqual(self.jw.get_raw_score(u'László', u'Lsáló'),
                               0.8900000000000001)
        self.assertAlmostEqual(self.jw.get_raw_score('László', 'Lsáló'),
                               0.8900000000000001)
        self.assertAlmostEqual(self.jw.get_raw_score(b'L\xc3\xa1szl\xc3\xb3',
                                                     b'Ls\xc3\xa1l\xc3\xb3'),
                               0.8900000000000001)

    def test_non_ascii_input_sim_score(self):
        self.assertAlmostEqual(self.jw.get_sim_score(u'MARTHA', u'MARHTA'),
                               0.9611111111111111)
        self.assertAlmostEqual(self.jw.get_sim_score(u'László', u'Lsáló'),
                               0.8900000000000001)
        self.assertAlmostEqual(self.jw.get_sim_score('László', 'Lsáló'),
                               0.8900000000000001)
        self.assertAlmostEqual(self.jw.get_sim_score(b'L\xc3\xa1szl\xc3\xb3',
                                                     b'Ls\xc3\xa1l\xc3\xb3'),
                               0.8900000000000001)

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.jw.get_raw_score(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.jw.get_raw_score('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.jw.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.jw.get_raw_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.jw.get_raw_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.jw.get_raw_score(12.90, 12.90)

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.jw.get_sim_score(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.jw.get_sim_score('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.jw.get_sim_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_sim_score(self):
        self.jw.get_sim_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_sim_score(self):
        self.jw.get_sim_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_sim_score(self):
        self.jw.get_sim_score(12.90, 12.90)