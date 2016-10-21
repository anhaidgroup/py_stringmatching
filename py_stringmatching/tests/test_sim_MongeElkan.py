# coding=utf-8

from __future__ import unicode_literals

import math
import unittest

from nose.tools import *

from py_stringmatching.similarity_measure.affine import Affine
from py_stringmatching.similarity_measure.jaro_winkler import JaroWinkler
from py_stringmatching.similarity_measure.monge_elkan import MongeElkan
from py_stringmatching.similarity_measure.needleman_wunsch import NeedlemanWunsch

class MongeElkanTestCases(unittest.TestCase):
    def setUp(self):
        self.me = MongeElkan()
        self.me_with_nw = MongeElkan(NeedlemanWunsch().get_raw_score)
        self.affine_fn = Affine().get_raw_score
        self.me_with_affine = MongeElkan(self.affine_fn)

    def test_get_sim_func(self):
        self.assertEqual(self.me_with_affine.get_sim_func(), self.affine_fn)

    def test_set_sim_func(self):
        fn1 = JaroWinkler().get_raw_score 
        fn2 = NeedlemanWunsch().get_raw_score
        me = MongeElkan(sim_func=fn1)
        self.assertEqual(me.get_sim_func(), fn1)
        self.assertAlmostEqual(me.get_raw_score(
                ['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            0.8364448051948052)
        self.assertEqual(me.set_sim_func(fn2), True)
        self.assertEqual(me.get_sim_func(), fn2)
        self.assertAlmostEqual(me.get_raw_score(
                ['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            2.0)

    def test_valid_input(self):
        self.assertEqual(self.me.get_raw_score([''], ['']), 1.0)  # need to check this

        self.assertEqual(self.me.get_raw_score([''], ['a']), 0.0)
        self.assertEqual(self.me.get_raw_score(['a'], ['a']), 1.0)

        self.assertEqual(self.me.get_raw_score(['Niall'], ['Neal']), 0.8049999999999999)
        self.assertEqual(self.me.get_raw_score(['Niall'], ['Njall']), 0.88)
        self.assertEqual(self.me.get_raw_score(
                ['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            0.8364448051948052)
        self.assertEqual(self.me_with_nw.get_raw_score(
                ['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']), 
            2.0)
        self.assertEqual(self.me_with_affine.get_raw_score(
                ['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            2.25)
        self.assertEqual(self.me.get_raw_score(['Niall'], ['Niel']), 0.8266666666666667)
        self.assertEqual(self.me.get_raw_score(['Niall'], ['Nigel']), 0.7866666666666667)
        self.assertEqual(self.me.get_raw_score([], ['Nigel']), 0.0)

    def test_valid_input_non_ascii(self):
        self.assertEqual(self.me.get_raw_score([u'Nóáll'], [u'Neál']), 0.8049999999999999)
        self.assertEqual(self.me.get_raw_score(['Nóáll'], ['Neál']), 0.8049999999999999)
        self.assertEqual(self.me.get_raw_score([b'N\xc3\xb3\xc3\xa1ll'], [b'Ne\xc3\xa1l']),
                         0.8049999999999999)

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.me.get_raw_score(1, 1)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.me.get_raw_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.me.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.me.get_raw_score("temp", "temp")

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.me.get_raw_score(['temp'], 'temp')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.me.get_raw_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input7_raw_score(self):
        self.me.get_raw_score('temp', ['temp'])