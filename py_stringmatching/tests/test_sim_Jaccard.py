# coding=utf-8

from __future__ import unicode_literals

import math
import unittest

from nose.tools import *

from py_stringmatching.similarity_measure.jaccard import Jaccard

class JaccardTestCases(unittest.TestCase):
    def setUp(self):
        self.jac = Jaccard()

    def test_valid_input_raw_score(self):
        self.assertEqual(self.jac.get_raw_score(['data', 'science'], ['data']),
                         1.0 / 2.0)
        self.assertEqual(self.jac.get_raw_score(['data', 'science'],
                                                ['science', 'good']), 1.0 / 3.0)
        self.assertEqual(self.jac.get_raw_score([], ['data']), 0)
        self.assertEqual(self.jac.get_raw_score(['data', 'data', 'science'],
                             ['data', 'management']), 1.0 / 3.0)
        self.assertEqual(self.jac.get_raw_score(['data', 'management'],
                             ['data', 'data', 'science']), 1.0 / 3.0)
        self.assertEqual(self.jac.get_raw_score([], []), 1.0)
        self.assertEqual(self.jac.get_raw_score(set([]), set([])), 1.0)
        self.assertEqual(self.jac.get_raw_score({1, 1, 2, 3, 4},
                             {2, 3, 4, 5, 6, 7, 7, 8}), 3.0 / 8.0)

    def test_valid_input_sim_score(self):
        self.assertEqual(self.jac.get_sim_score(['data', 'science'], ['data']),
                         1.0 / 2.0)
        self.assertEqual(self.jac.get_sim_score(['data', 'science'],
                                                ['science', 'good']), 1.0 / 3.0)
        self.assertEqual(self.jac.get_sim_score([], ['data']), 0)
        self.assertEqual(self.jac.get_sim_score(['data', 'data', 'science'],
                             ['data', 'management']), 1.0 / 3.0)
        self.assertEqual(self.jac.get_sim_score(['data', 'management'],
                             ['data', 'data', 'science']), 1.0 / 3.0)
        self.assertEqual(self.jac.get_sim_score([], []), 1.0)
        self.assertEqual(self.jac.get_sim_score(set([]), set([])), 1.0)
        self.assertEqual(self.jac.get_sim_score({1, 1, 2, 3, 4},
                             {2, 3, 4, 5, 6, 7, 7, 8}), 3.0 / 8.0)

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.jac.get_raw_score(1, 1)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.jac.get_raw_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.jac.get_raw_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.jac.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.jac.get_raw_score(['MARHTA'], 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.jac.get_raw_score('MARHTA', ['MARTHA'])

    @raises(TypeError)
    def test_invalid_input7_raw_score(self):
        self.jac.get_raw_score('MARTHA', 'MARTHA')

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.jac.get_sim_score(1, 1)

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.jac.get_sim_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.jac.get_sim_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input4_sim_score(self):
        self.jac.get_sim_score(None, None)

    @raises(TypeError)
    def test_invalid_input5_sim_score(self):
        self.jac.get_sim_score(['MARHTA'], 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_sim_score(self):
        self.jac.get_sim_score('MARHTA', ['MARTHA'])

    @raises(TypeError)
    def test_invalid_input7_sim_score(self):
        self.jac.get_sim_score('MARTHA', 'MARTHA')