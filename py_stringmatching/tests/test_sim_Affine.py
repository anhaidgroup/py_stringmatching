# coding=utf-8

from __future__ import unicode_literals

import math
import unittest

from nose.tools import *
from py_stringmatching.similarity_measure.affine import Affine

class AffineTestCases(unittest.TestCase):
    def setUp(self):
        self.affine = Affine()
        self.affine_with_params1 = Affine(gap_start=2, gap_continuation=0.5)
        self.sim_func = lambda s1, s2: (int(1 if s1 == s2 else 0))
        self.affine_with_params2 = Affine(gap_continuation=0.2, sim_func=self.sim_func)

    def test_valid_input(self):
        self.assertAlmostEqual(self.affine.get_raw_score('dva', 'deeva'), 1.5)
        self.assertAlmostEqual(self.affine_with_params1.get_raw_score('dva', 'deeve'), -0.5)
        self.assertAlmostEqual(self.affine_with_params2.get_raw_score('AAAGAATTCA', 'AAATCA'),
                               4.4)
        self.assertAlmostEqual(self.affine_with_params2.get_raw_score(' ', ' '), 1)
        self.assertEqual(self.affine.get_raw_score('', 'deeva'), 0)

    def test_valid_input_non_ascii(self):
        self.assertAlmostEqual(self.affine.get_raw_score(u'dva', u'dáóva'), 1.5)
        self.assertAlmostEqual(self.affine.get_raw_score('dva', 'dáóva'), 1.5)
        self.assertAlmostEqual(self.affine.get_raw_score('dva', b'd\xc3\xa1\xc3\xb3va'), 1.5)

    def test_get_gap_start(self):
        self.assertEqual(self.affine_with_params1.get_gap_start(), 2)

    def test_get_gap_continuation(self):
        self.assertEqual(self.affine_with_params2.get_gap_continuation(), 0.2)

    def test_get_sim_func(self):
        self.assertEqual(self.affine_with_params2.get_sim_func(), self.sim_func)

    def test_set_gap_start(self):
        af = Affine(gap_start=1)
        self.assertEqual(af.get_gap_start(), 1)
        self.assertAlmostEqual(af.get_raw_score('dva', 'deeva'), 1.5)
        self.assertEqual(af.set_gap_start(2), True)
        self.assertEqual(af.get_gap_start(), 2)
        self.assertAlmostEqual(af.get_raw_score('dva', 'deeva'), 0.5)

    def test_set_gap_continuation(self):
        af = Affine(gap_continuation=0.3)
        self.assertEqual(af.get_gap_continuation(), 0.3)
        self.assertAlmostEqual(af.get_raw_score('dva', 'deeva'), 1.7)
        self.assertEqual(af.set_gap_continuation(0.7), True)
        self.assertEqual(af.get_gap_continuation(), 0.7)
        self.assertAlmostEqual(af.get_raw_score('dva', 'deeva'), 1.3)

    def test_set_sim_func(self):
        fn1 = lambda s1, s2: (int(1 if s1 == s2 else 0))
        fn2 = lambda s1, s2: (int(2 if s1 == s2 else -1))
        af = Affine(sim_func=fn1)
        self.assertEqual(af.get_sim_func(), fn1)
        self.assertAlmostEqual(af.get_raw_score('dva', 'deeva'), 1.5)
        self.assertEqual(af.set_sim_func(fn2), True)
        self.assertEqual(af.get_sim_func(), fn2)
        self.assertAlmostEqual(af.get_raw_score('dva', 'deeva'), 4.5)

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.affine.get_raw_score(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.affine.get_raw_score('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.affine.get_raw_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.affine.get_raw_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.affine.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.affine.get_raw_score(12.90, 12.90)