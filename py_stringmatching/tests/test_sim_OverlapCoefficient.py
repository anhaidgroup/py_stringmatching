# coding=utf-8

from __future__ import unicode_literals

import math
import unittest

from nose.tools import *

from py_stringmatching.similarity_measure.overlap_coefficient import OverlapCoefficient

class OverlapCoefficientTestCases(unittest.TestCase):
    def setUp(self):
        self.oc = OverlapCoefficient()

    def test_valid_input_raw_score(self):
        self.assertEqual(self.oc.get_raw_score([], []), 1.0)
        self.assertEqual(self.oc.get_raw_score(['data', 'science'], ['data']),
                         1.0 / min(2.0, 1.0))
        self.assertEqual(self.oc.get_raw_score(['data', 'science'],
                                               ['science', 'good']), 1.0 / min(2.0, 3.0))
        self.assertEqual(self.oc.get_raw_score([], ['data']), 0)
        self.assertEqual(self.oc.get_raw_score(['data', 'data', 'science'],
                                               ['data', 'management']), 1.0 / min(3.0, 2.0))

    def test_valid_input_raw_score_set_inp(self):
        self.assertEqual(self.oc.get_raw_score(set(['data', 'science']), set(['data'])),
                         1.0 / min(2.0, 1.0))

    def test_valid_input_sim_score(self):
        self.assertEqual(self.oc.get_sim_score([], []), 1.0)
        self.assertEqual(self.oc.get_sim_score(['data', 'science'], ['data']),
                         1.0 / min(2.0, 1.0))
        self.assertEqual(self.oc.get_sim_score(['data', 'science'],
                                               ['science', 'good']), 1.0 / min(2.0, 3.0))
        self.assertEqual(self.oc.get_sim_score([], ['data']), 0)
        self.assertEqual(self.oc.get_sim_score(['data', 'data', 'science'],
                                               ['data', 'management']), 1.0 / min(3.0, 2.0))

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.oc.get_raw_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.oc.get_raw_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.oc.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.oc.get_raw_score(['MARHTA'], 'MARTHA')

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.oc.get_raw_score('MARHTA', ['MARTHA'])

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.oc.get_raw_score('MARTHA', 'MARTHA')

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.oc.get_sim_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.oc.get_sim_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.oc.get_sim_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_sim_score(self):
        self.oc.get_sim_score(['MARHTA'], 'MARTHA')

    @raises(TypeError)
    def test_invalid_input5_sim_score(self):
        self.oc.get_sim_score('MARHTA', ['MARTHA'])

    @raises(TypeError)
    def test_invalid_input6_sim_score(self):
        self.oc.get_sim_score('MARTHA', 'MARTHA')