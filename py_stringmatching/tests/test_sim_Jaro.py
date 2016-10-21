# coding=utf-8

from __future__ import unicode_literals

import math
import unittest

from nose.tools import *

from py_stringmatching.similarity_measure.jaro import Jaro

class JaroTestCases(unittest.TestCase):
    def setUp(self):
        self.jaro = Jaro()

    def test_valid_input_raw_score(self):
        # https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance
        self.assertAlmostEqual(self.jaro.get_raw_score('MARTHA', 'MARHTA'),
                               0.9444444444444445)
        self.assertAlmostEqual(self.jaro.get_raw_score('DWAYNE', 'DUANE'),
                               0.8222222222222223)
        self.assertAlmostEqual(self.jaro.get_raw_score('DIXON', 'DICKSONX'),
                               0.7666666666666666)
        self.assertEqual(self.jaro.get_raw_score('', 'deeva'), 0)

    def test_valid_input_sim_score(self):
        self.assertAlmostEqual(self.jaro.get_sim_score('MARTHA', 'MARHTA'),
                               0.9444444444444445)
        self.assertAlmostEqual(self.jaro.get_sim_score('DWAYNE', 'DUANE'),
                               0.8222222222222223)
        self.assertAlmostEqual(self.jaro.get_sim_score('DIXON', 'DICKSONX'),
                               0.7666666666666666)
        self.assertEqual(self.jaro.get_sim_score('', 'deeva'), 0)

    def test_non_ascii_input_raw_score(self):
        self.assertAlmostEqual(self.jaro.get_raw_score(u'MARTHA', u'MARHTA'),
                               0.9444444444444445)
        self.assertAlmostEqual(self.jaro.get_raw_score(u'László', u'Lsáló'),
                               0.8777777777777779)
        self.assertAlmostEqual(self.jaro.get_raw_score('László', 'Lsáló'),
                               0.8777777777777779)
        self.assertAlmostEqual(self.jaro.get_raw_score(b'L\xc3\xa1szl\xc3\xb3',
                                                       b'Ls\xc3\xa1l\xc3\xb3'),
                               0.8777777777777779)

    def test_non_ascii_input_sim_score(self):
        self.assertAlmostEqual(self.jaro.get_sim_score(u'MARTHA', u'MARHTA'),
                               0.9444444444444445)
        self.assertAlmostEqual(self.jaro.get_sim_score(u'László', u'Lsáló'),
                               0.8777777777777779)
        self.assertAlmostEqual(self.jaro.get_sim_score('László', 'Lsáló'),
                               0.8777777777777779)
        self.assertAlmostEqual(self.jaro.get_sim_score(b'L\xc3\xa1szl\xc3\xb3',
                                                       b'Ls\xc3\xa1l\xc3\xb3'),
                               0.8777777777777779)

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.jaro.get_raw_score(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.jaro.get_raw_score('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.jaro.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.jaro.get_raw_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.jaro.get_raw_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.jaro.get_raw_score(12.90, 12.90)

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.jaro.get_sim_score(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.jaro.get_sim_score('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.jaro.get_sim_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_sim_score(self):
        self.jaro.get_sim_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_sim_score(self):
        self.jaro.get_sim_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_sim_score(self):
        self.jaro.get_sim_score(12.90, 12.90)