# coding=utf-8

from __future__ import unicode_literals

import math
import unittest

from nose.tools import *

from py_stringmatching.similarity_measure.tversky_index import TverskyIndex

class TverskyIndexTestCases(unittest.TestCase):
    def setUp(self):
        self.tvi = TverskyIndex()
        self.tvi_with_params1 = TverskyIndex(0.5, 0.5)
        self.tvi_with_params2 = TverskyIndex(0.7, 0.8)
        self.tvi_with_params3 = TverskyIndex(0.2, 0.4)
        self.tvi_with_params4 = TverskyIndex(0.9, 0.8)
        self.tvi_with_params5 = TverskyIndex(0.45, 0.85)

    def test_get_alpha(self):
        self.assertEqual(self.tvi_with_params5.get_alpha(), 0.45)

    def test_get_beta(self):
        self.assertEqual(self.tvi_with_params5.get_beta(), 0.85)

    def test_set_alpha(self):
        tvi = TverskyIndex(alpha=0.3)
        self.assertEqual(tvi.get_alpha(), 0.3)
        self.assertAlmostEqual(tvi.get_raw_score(['data', 'science'], ['data']),
                               0.7692307692307692)
        self.assertEqual(tvi.set_alpha(0.7), True)
        self.assertEqual(tvi.get_alpha(), 0.7)
        self.assertAlmostEqual(tvi.get_raw_score(['data', 'science'], ['data']),
                               0.5882352941176471)

    def test_set_beta(self):
        tvi = TverskyIndex(beta=0.3)
        self.assertEqual(tvi.get_beta(), 0.3)
        self.assertAlmostEqual(tvi.get_raw_score(['data', 'science'], ['science', 'good']),
                               0.5555555555555556)
        self.assertEqual(tvi.set_beta(0.7), True)
        self.assertEqual(tvi.get_beta(), 0.7)
        self.assertAlmostEqual(tvi.get_raw_score(['data', 'science'], ['science', 'good']),
                               0.45454545454545453)

    def test_valid_input_raw_score(self):
        self.assertEqual(self.tvi_with_params1.get_raw_score(['data', 'science'], ['data']),
                         1.0 / (1.0 + 0.5*1 + 0.5*0))
        self.assertEqual(self.tvi.get_raw_score(['data', 'science'], ['science', 'good']),
                         1.0 / (1.0 + 0.5*1 + 0.5*1))
        self.assertEqual(self.tvi.get_raw_score([], ['data']), 0)
        self.assertEqual(self.tvi_with_params2.get_raw_score(['data', 'data', 'science'],
                                                             ['data', 'management']),
                         1.0 / (1.0 + 0.7*1 + 0.8*1))
        self.assertEqual(self.tvi_with_params3.get_raw_score(['data', 'management', 'science'],
                                                             ['data', 'data', 'science']),
                         2.0 / (2.0 + 0.2*1 + 0))
        self.assertEqual(self.tvi.get_raw_score([], []), 1.0)
        self.assertEqual(self.tvi_with_params4.get_raw_score(['a', 'b'], ['b', 'a']), 1.0)
        self.assertEqual(self.tvi.get_raw_score(['a', 'b'], ['b', 'a']), 1.0)
        self.assertEqual(self.tvi.get_raw_score(set([]), set([])), 1.0)
        self.assertEqual(self.tvi_with_params5.get_raw_score({1, 1, 2, 3, 4}, {2, 3, 4, 5, 6, 7, 7, 8}),
                         3.0 / (3.0 + 0.45*1 + 0.85*4))

    def test_valid_input_sim_score(self):
        self.assertEqual(self.tvi_with_params1.get_sim_score(['data', 'science'], ['data']),
                         1.0 / (1.0 + 0.5*1 + 0.5*0))
        self.assertEqual(self.tvi.get_sim_score(['data', 'science'], ['science', 'good']),
                         1.0 / (1.0 + 0.5*1 + 0.5*1))
        self.assertEqual(self.tvi.get_sim_score([], ['data']), 0)
        self.assertEqual(self.tvi_with_params2.get_sim_score(['data', 'data', 'science'],
                                                             ['data', 'management']),
                         1.0 / (1.0 + 0.7*1 + 0.8*1))
        self.assertEqual(self.tvi_with_params3.get_sim_score(['data', 'management', 'science'],
                                                             ['data', 'data', 'science']),
                         2.0 / (2.0 + 0.2*1 + 0))
        self.assertEqual(self.tvi.get_sim_score([], []), 1.0)
        self.assertEqual(self.tvi_with_params4.get_sim_score(['a', 'b'], ['b', 'a']), 1.0)
        self.assertEqual(self.tvi.get_sim_score(['a', 'b'], ['b', 'a']), 1.0)
        self.assertEqual(self.tvi.get_sim_score(set([]), set([])), 1.0)
        self.assertEqual(self.tvi_with_params5.get_sim_score({1, 1, 2, 3, 4}, {2, 3, 4, 5, 6, 7, 7, 8}),
                         3.0 / (3.0 + 0.45*1 + 0.85*4))

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.tvi.get_raw_score(1, 1)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.tvi.get_raw_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.tvi.get_raw_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.tvi.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.tvi.get_raw_score(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.tvi.get_raw_score('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input7_raw_score(self):
        self.tvi.get_raw_score('MARHTA', 'MARTHA')

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.tvi.get_sim_score(1, 1)

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.tvi.get_sim_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.tvi.get_sim_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input4_sim_score(self):
        self.tvi.get_sim_score(None, None)

    @raises(TypeError)
    def test_invalid_input5_sim_score(self):
        self.tvi.get_sim_score(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input6_sim_score(self):
        self.tvi.get_sim_score('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input7_sim_score(self):
        self.tvi.get_sim_score('MARHTA', 'MARTHA')

    @raises(ValueError)
    def test_invalid_input8(self):
        tvi_invalid = TverskyIndex(0.5, -0.9)

    @raises(ValueError)
    def test_invalid_input9(self):
        tvi_invalid = TverskyIndex(-0.5, 0.9)

    @raises(ValueError)
    def test_invalid_input10(self):
        tvi_invalid = TverskyIndex(-0.5, -0.9)