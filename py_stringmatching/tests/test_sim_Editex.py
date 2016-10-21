# coding=utf-8

from __future__ import unicode_literals

import math
import unittest

from nose.tools import *

from py_stringmatching.similarity_measure.editex import Editex

class EditexTestCases(unittest.TestCase):
    def setUp(self):
        self.ed = Editex()
        self.ed_with_params1 = Editex(match_cost=2)
        self.ed_with_params2 = Editex(mismatch_cost=2)
        self.ed_with_params3 = Editex(mismatch_cost=1)
        self.ed_with_params4 = Editex(mismatch_cost=3, group_cost=2)
        self.ed_with_params5 = Editex(mismatch_cost=3, group_cost=2, local=True)
        self.ed_with_params6 = Editex(local=True)

    def test_get_match_cost(self):
        self.assertEqual(self.ed_with_params1.get_match_cost(), 2)

    def test_get_group_cost(self):
        self.assertEqual(self.ed_with_params4.get_group_cost(), 2)

    def test_get_mismatch_cost(self):
        self.assertEqual(self.ed_with_params4.get_mismatch_cost(), 3)

    def test_get_local(self):
        self.assertEqual(self.ed_with_params5.get_local(), True)

    def test_set_match_cost(self):
        ed = Editex(match_cost=2)
        self.assertEqual(ed.get_match_cost(), 2)
        self.assertAlmostEqual(ed.get_raw_score('MARTHA', 'MARHTA'), 12)
        self.assertEqual(ed.set_match_cost(4), True)
        self.assertEqual(ed.get_match_cost(), 4)
        self.assertAlmostEqual(ed.get_raw_score('MARTHA', 'MARHTA'), 14)

    def test_set_group_cost(self):
        ed = Editex(group_cost=1)
        self.assertEqual(ed.get_group_cost(), 1)
        self.assertAlmostEqual(ed.get_raw_score('MARTHA', 'MARHTA'), 3)
        self.assertEqual(ed.set_group_cost(2), True)
        self.assertEqual(ed.get_group_cost(), 2)
        self.assertAlmostEqual(ed.get_raw_score('MARTHA', 'MARHTA'), 4)

    def test_set_mismatch_cost(self):
        ed = Editex(mismatch_cost=2)
        self.assertEqual(ed.get_mismatch_cost(), 2)
        self.assertAlmostEqual(ed.get_raw_score('MARTHA', 'MARHTA'), 3)
        self.assertEqual(ed.set_mismatch_cost(4), True)
        self.assertEqual(ed.get_mismatch_cost(), 4)
        self.assertAlmostEqual(ed.get_raw_score('MARTHA', 'MARHTA'), 5)

    def test_set_local(self):
        ed = Editex(local=False)
        self.assertEqual(ed.get_local(), False)
        self.assertAlmostEqual(ed.get_raw_score('MARTHA', 'MARHTA'), 3)
        self.assertEqual(ed.set_local(True), True)
        self.assertEqual(ed.get_local(), True)
        self.assertAlmostEqual(ed.get_raw_score('MARTHA', 'MARHTA'), 3)

    def test_valid_input_raw_score(self):
        self.assertEqual(self.ed.get_raw_score('MARTHA', 'MARTHA'), 0)
        self.assertEqual(self.ed.get_raw_score('MARTHA', 'MARHTA'), 3)
        self.assertEqual(self.ed.get_raw_score('ALIE', 'ALI'), 1)
        self.assertEqual(self.ed_with_params1.get_raw_score('ALIE', 'ALI'), 7)
        self.assertEqual(self.ed_with_params2.get_raw_score('ALIE', 'ALIF'), 2)
        self.assertEqual(self.ed_with_params3.get_raw_score('ALIE', 'ALIF'), 1)
        self.assertEqual(self.ed_with_params4.get_raw_score('ALIP', 'ALIF'), 2)
        self.assertEqual(self.ed_with_params4.get_raw_score('ALIe', 'ALIF'), 3)
        self.assertEqual(self.ed_with_params5.get_raw_score('WALIW', 'HALIH'), 6)
        self.assertEqual(self.ed_with_params6.get_raw_score('niall', 'nihal'), 2)
        self.assertEqual(self.ed_with_params6.get_raw_score('nihal', 'niall'), 2)
        self.assertEqual(self.ed_with_params6.get_raw_score('neal', 'nihl'), 3)
        self.assertEqual(self.ed_with_params6.get_raw_score('nihl', 'neal'), 3)
        self.assertEqual(self.ed.get_raw_score('', ''), 0)
        self.assertEqual(self.ed.get_raw_score('', 'MARTHA'), 12)
        self.assertEqual(self.ed.get_raw_score('MARTHA', ''), 12)

    def test_valid_input_sim_score(self):
        self.assertEqual(self.ed.get_sim_score('MARTHA', 'MARTHA'), 1.0)
        self.assertEqual(self.ed.get_sim_score('MARTHA', 'MARHTA'), 1.0 - (3.0/12.0))
        self.assertEqual(self.ed.get_sim_score('ALIE', 'ALI'), 1.0 - (1.0/8.0))
        self.assertEqual(self.ed_with_params1.get_sim_score('ALIE', 'ALI'), 1.0 - (7.0/8.0))
        self.assertEqual(self.ed_with_params2.get_sim_score('ALIE', 'ALIF'), 1.0 - (2.0/8.0))
        self.assertEqual(self.ed_with_params3.get_sim_score('ALIE', 'ALIF'), 1.0 - (1.0/4.0))
        self.assertEqual(self.ed_with_params4.get_sim_score('ALIP', 'ALIF'), 1.0 - (2.0/12.0))
        self.assertEqual(self.ed_with_params4.get_sim_score('ALIe', 'ALIF'), 1.0 - (3.0/12.0))
        self.assertEqual(self.ed_with_params5.get_sim_score('WALIW', 'HALIH'), 1.0 - (6.0/15.0))
        self.assertEqual(self.ed_with_params6.get_sim_score('niall', 'nihal'), 1.0 - (2.0/10.0))
        self.assertEqual(self.ed_with_params6.get_sim_score('nihal', 'niall'), 1.0 - (2.0/10.0))
        self.assertEqual(self.ed_with_params6.get_sim_score('neal', 'nihl'), 1.0 - (3.0/8.0))
        self.assertEqual(self.ed_with_params6.get_sim_score('nihl', 'neal'), 1.0 - (3.0/8.0))
        self.assertEqual(self.ed.get_sim_score('', ''), 1.0)

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.ed.get_raw_score(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.ed.get_raw_score('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.ed.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.ed.get_raw_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.ed.get_raw_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.ed.get_raw_score(12.90, 12.90)

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.ed.get_sim_score(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.ed.get_sim_score('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.ed.get_sim_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_sim_score(self):
        self.ed.get_sim_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_sim_score(self):
        self.ed.get_sim_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_sim_score(self):
        self.ed.get_sim_score(12.90, 12.90)