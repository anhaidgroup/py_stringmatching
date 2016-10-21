# coding=utf-8

from __future__ import unicode_literals

import math
import unittest

from nose.tools import *

from py_stringmatching.similarity_measure.needleman_wunsch import NeedlemanWunsch

class NeedlemanWunschTestCases(unittest.TestCase):
    def setUp(self):
        self.nw = NeedlemanWunsch()
        self.nw_with_params1 = NeedlemanWunsch(0.0)
        self.nw_with_params2 = NeedlemanWunsch(1.0,
            sim_func=lambda s1, s2: (2 if s1 == s2 else -1))
        self.sim_func=lambda s1, s2: (1 if s1 == s2 else -1)
        self.nw_with_params3 = NeedlemanWunsch(gap_cost=0.5,
                                   sim_func=self.sim_func)

    def test_get_gap_cost(self):
        self.assertEqual(self.nw_with_params3.get_gap_cost(), 0.5)

    def test_get_sim_func(self):
        self.assertEqual(self.nw_with_params3.get_sim_func(), self.sim_func)

    def test_set_gap_cost(self):
        nw = NeedlemanWunsch(gap_cost=0.5)
        self.assertEqual(nw.get_gap_cost(), 0.5)
        self.assertAlmostEqual(nw.get_raw_score('dva', 'deeva'), 2.0)
        self.assertEqual(nw.set_gap_cost(0.7), True)
        self.assertEqual(nw.get_gap_cost(), 0.7)
        self.assertAlmostEqual(nw.get_raw_score('dva', 'deeva'), 1.6000000000000001)

    def test_set_sim_func(self):
        fn1 = lambda s1, s2: (int(1 if s1 == s2 else 0))
        fn2 = lambda s1, s2: (int(2 if s1 == s2 else -1))
        nw = NeedlemanWunsch(sim_func=fn1)
        self.assertEqual(nw.get_sim_func(), fn1)
        self.assertAlmostEqual(nw.get_raw_score('dva', 'deeva'), 1.0)
        self.assertEqual(nw.set_sim_func(fn2), True)
        self.assertEqual(nw.get_sim_func(), fn2)
        self.assertAlmostEqual(nw.get_raw_score('dva', 'deeva'), 4.0)

    def test_valid_input(self):
        self.assertEqual(self.nw.get_raw_score('dva', 'deeva'), 1.0)
        self.assertEqual(self.nw_with_params1.get_raw_score('dva', 'deeve'), 2.0)
        self.assertEqual(self.nw_with_params2.get_raw_score('dva', 'deeve'), 1.0)
        self.assertEqual(self.nw_with_params3.get_raw_score('GCATGCUA', 'GATTACA'),
                         2.5)

    def test_valid_input_non_ascii(self):
        self.assertEqual(self.nw.get_raw_score(u'dva', u'dáóva'), 1.0)
        self.assertEqual(self.nw.get_raw_score('dva', 'dáóva'), 1.0)
        self.assertEqual(self.nw.get_raw_score('dva', b'd\xc3\xa1\xc3\xb3va'), 1.0)

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.nw.get_raw_score('a', None)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.nw.get_raw_score(None, 'b')

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.nw.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.nw.get_raw_score(['a'], 'b')

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.nw.get_raw_score('a', ['b'])

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.nw.get_raw_score(['a'], ['b'])