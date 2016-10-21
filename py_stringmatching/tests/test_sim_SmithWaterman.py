# coding=utf-8

from __future__ import unicode_literals

import math
import unittest

from nose.tools import *

from py_stringmatching.similarity_measure.smith_waterman import SmithWaterman

class SmithWatermanTestCases(unittest.TestCase):
    def setUp(self):
        self.sw = SmithWaterman()
        self.sw_with_params1 = SmithWaterman(2.2)
        self.sw_with_params2 = SmithWaterman(1,
            sim_func=lambda s1, s2: (2 if s1 == s2 else -1))
        self.sw_with_params3 = SmithWaterman(gap_cost=1,
            sim_func=lambda s1, s2: (int(1 if s1 == s2 else -1)))
        self.sim_func=lambda s1, s2: (1.5 if s1 == s2 else 0.5)
        self.sw_with_params4 = SmithWaterman(gap_cost=1.4,
                                   sim_func=self.sim_func)

    def test_get_gap_cost(self):
        self.assertEqual(self.sw_with_params4.get_gap_cost(), 1.4)

    def test_get_sim_func(self):
        self.assertEqual(self.sw_with_params4.get_sim_func(), self.sim_func)

    def test_set_gap_cost(self):
        sw = SmithWaterman(gap_cost=0.3)
        self.assertEqual(sw.get_gap_cost(), 0.3)
        self.assertAlmostEqual(sw.get_raw_score('dva', 'deeva'), 2.3999999999999999)
        self.assertEqual(sw.set_gap_cost(0.7), True)
        self.assertEqual(sw.get_gap_cost(), 0.7)
        self.assertAlmostEqual(sw.get_raw_score('dva', 'deeva'), 2.0)

    def test_set_sim_func(self):
        fn1 = lambda s1, s2: (int(1 if s1 == s2 else 0))
        fn2 = lambda s1, s2: (int(2 if s1 == s2 else -1))
        sw = SmithWaterman(sim_func=fn1)
        self.assertEqual(sw.get_sim_func(), fn1)
        self.assertAlmostEqual(sw.get_raw_score('dva', 'deeva'), 2.0)
        self.assertEqual(sw.set_sim_func(fn2), True)
        self.assertEqual(sw.get_sim_func(), fn2)
        self.assertAlmostEqual(sw.get_raw_score('dva', 'deeva'), 4.0)

    def test_valid_input(self):
        self.assertEqual(self.sw.get_raw_score('cat', 'hat'), 2.0)
        self.assertEqual(self.sw_with_params1.get_raw_score('dva', 'deeve'), 1.0)
        self.assertEqual(self.sw_with_params2.get_raw_score('dva', 'deeve'), 2.0)
        self.assertEqual(self.sw_with_params3.get_raw_score('GCATGCU', 'GATTACA'),
                         2.0)
        self.assertEqual(self.sw_with_params4.get_raw_score('GCATAGCU', 'GATTACA'),
                         6.5)

    def test_valid_input_non_ascii(self):
        self.assertEqual(self.sw.get_raw_score(u'óát', u'cát'), 2.0)
        self.assertEqual(self.sw.get_raw_score('óát', 'cát'), 2.0)
        self.assertEqual(self.sw.get_raw_score(b'\xc3\xb3\xc3\xa1t', b'c\xc3\xa1t'), 
                         2.0)

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.sw.get_raw_score('a', None)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.sw.get_raw_score(None, 'b')

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.sw.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.sw.get_raw_score('MARHTA', 12)

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.sw.get_raw_score(12, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.sw.get_raw_score(12, 12)