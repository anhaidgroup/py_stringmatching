# coding=utf-8

from __future__ import unicode_literals

import math
import unittest

from nose.tools import *

from py_stringmatching.similarity_measure.generalized_jaccard import GeneralizedJaccard
from py_stringmatching.similarity_measure.jaro_winkler import JaroWinkler
from py_stringmatching.similarity_measure.needleman_wunsch import NeedlemanWunsch
from py_stringmatching.similarity_measure.jaro import Jaro

class GeneralizedJaccardTestCases(unittest.TestCase):
    def setUp(self):
        self.gen_jac = GeneralizedJaccard()
        self.jw_fn = JaroWinkler().get_raw_score
        self.gen_jac_with_jw = GeneralizedJaccard(sim_func=self.jw_fn)
        self.gen_jac_with_jw_08 = GeneralizedJaccard(sim_func=self.jw_fn,
                                                     threshold=0.8)
        self.gen_jac_invalid = GeneralizedJaccard(sim_func=NeedlemanWunsch().get_raw_score,
                                                  threshold=0.8)

    def test_get_sim_func(self):
        self.assertEqual(self.gen_jac_with_jw_08.get_sim_func(), self.jw_fn)

    def test_get_threshold(self):
        self.assertEqual(self.gen_jac_with_jw_08.get_threshold(), 0.8)

    def test_set_threshold(self):
        gj = GeneralizedJaccard(threshold=0.8)
        self.assertEqual(gj.get_threshold(), 0.8)
        self.assertAlmostEqual(gj.get_raw_score(['Niall'], ['Neal', 'Njall']), 0.43333333333333335)
        self.assertEqual(gj.set_threshold(0.9), True)
        self.assertEqual(gj.get_threshold(), 0.9)
        self.assertAlmostEqual(gj.get_raw_score(['Niall'], ['Neal', 'Njall']), 0.0)

    def test_set_sim_func(self):
        fn1 = JaroWinkler().get_raw_score
        fn2 = Jaro().get_raw_score
        gj = GeneralizedJaccard(sim_func=fn1)
        self.assertEqual(gj.get_sim_func(), fn1)
        self.assertAlmostEqual(gj.get_raw_score(['Niall'], ['Neal', 'Njall']), 0.44)
        self.assertEqual(gj.set_sim_func(fn2), True)
        self.assertEqual(gj.get_sim_func(), fn2)
        self.assertAlmostEqual(gj.get_raw_score(['Niall'], ['Neal', 'Njall']), 0.43333333333333335)

    def test_valid_input_raw_score(self):
        self.assertEqual(self.gen_jac.get_raw_score([''], ['']), 1.0)  # need to check this

        self.assertEqual(self.gen_jac.get_raw_score([''], ['a']), 0.0)
        self.assertEqual(self.gen_jac.get_raw_score(['a'], ['a']), 1.0)

        self.assertEqual(self.gen_jac.get_raw_score([], ['Nigel']), 0.0)
        self.assertEqual(self.gen_jac.get_raw_score(['Niall'], ['Neal']), 0.7833333333333333)
        self.assertEqual(self.gen_jac.get_raw_score(['Niall'], ['Njall', 'Neal']), 0.43333333333333335)
        self.assertEqual(self.gen_jac.get_raw_score(['Niall'], ['Neal', 'Njall']), 0.43333333333333335)
        self.assertEqual(self.gen_jac.get_raw_score(
                ['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            0.6800468975468975)

        self.assertEqual(self.gen_jac_with_jw.get_raw_score(
                ['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            0.7220003607503608)
        self.assertEqual(self.gen_jac_with_jw.get_raw_score(
                ['Comp', 'Sci.', 'and', 'Engr', 'Dept.,', 'Universty', 'of', 'Cal,', 'San', 'Deigo'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            0.7075277777777778)

        self.assertEqual(self.gen_jac_with_jw_08.get_raw_score(
                ['Comp', 'Sci.', 'and', 'Engr', 'Dept.,', 'Universty', 'of', 'Cal,', 'San', 'Deigo'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            0.45810185185185187)

    def test_valid_input_sim_score(self):
        self.assertEqual(self.gen_jac.get_sim_score([''], ['']), 1.0)  # need to check this

        self.assertEqual(self.gen_jac.get_sim_score([''], ['a']), 0.0)
        self.assertEqual(self.gen_jac.get_sim_score(['a'], ['a']), 1.0)

        self.assertEqual(self.gen_jac.get_sim_score([], ['Nigel']), 0.0)
        self.assertEqual(self.gen_jac.get_sim_score(['Niall'], ['Neal']), 0.7833333333333333)
        self.assertEqual(self.gen_jac.get_sim_score(['Niall'], ['Njall', 'Neal']), 0.43333333333333335)
        self.assertEqual(self.gen_jac.get_sim_score(['Niall'], ['Neal', 'Njall']), 0.43333333333333335)
        self.assertEqual(self.gen_jac.get_sim_score(
                ['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            0.6800468975468975)

        self.assertEqual(self.gen_jac_with_jw.get_sim_score(
                ['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            0.7220003607503608)
        self.assertEqual(self.gen_jac_with_jw.get_sim_score(
                ['Comp', 'Sci.', 'and', 'Engr', 'Dept.,', 'Universty', 'of', 'Cal,', 'San', 'Deigo'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            0.7075277777777778)

        self.assertEqual(self.gen_jac_with_jw_08.get_sim_score(
                ['Comp', 'Sci.', 'and', 'Engr', 'Dept.,', 'Universty', 'of', 'Cal,', 'San', 'Deigo'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            0.45810185185185187)

    def test_valid_input_non_ascii_raw_score(self):
        self.assertEqual(self.gen_jac.get_raw_score([u'Nóáll'], [u'Neál']), 0.7833333333333333)
        self.assertEqual(self.gen_jac.get_raw_score(['Nóáll'], ['Neál']), 0.7833333333333333)
        self.assertEqual(self.gen_jac.get_raw_score([b'N\xc3\xb3\xc3\xa1ll'], [b'Ne\xc3\xa1l']),
                         0.7833333333333333)

    def test_valid_input_non_ascii_sim_score(self):
        self.assertEqual(self.gen_jac.get_sim_score([u'Nóáll'], [u'Neál']), 0.7833333333333333)
        self.assertEqual(self.gen_jac.get_sim_score(['Nóáll'], ['Neál']), 0.7833333333333333)
        self.assertEqual(self.gen_jac.get_sim_score([b'N\xc3\xb3\xc3\xa1ll'], [b'Ne\xc3\xa1l']),
                         0.7833333333333333)

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.gen_jac.get_raw_score(1, 1)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.gen_jac.get_raw_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.gen_jac.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.gen_jac.get_raw_score("temp", "temp")

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.gen_jac.get_raw_score(['temp'], 'temp')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.gen_jac.get_raw_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input7_raw_score(self):
        self.gen_jac.get_raw_score('temp', ['temp'])

    @raises(ValueError)
    def test_invalid_sim_measure(self):
        self.gen_jac_invalid.get_raw_score(
                ['Comp', 'Sci.', 'and', 'Engr', 'Dept.,', 'Universty', 'of', 'Cal,', 'San', 'Deigo'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego'])

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.gen_jac.get_sim_score(1, 1)

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.gen_jac.get_sim_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.gen_jac.get_sim_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_sim_score(self):
        self.gen_jac.get_sim_score("temp", "temp")

    @raises(TypeError)
    def test_invalid_input5_sim_score(self):
        self.gen_jac.get_sim_score(['temp'], 'temp')

    @raises(TypeError)
    def test_invalid_input6_sim_score(self):
        self.gen_jac.get_sim_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input7_sim_score(self):
        self.gen_jac.get_sim_score('temp', ['temp'])

    @raises(ValueError)
    def test_invalid_sim_measure_sim_score(self):
        self.gen_jac_invalid.get_sim_score(
                ['Comp', 'Sci.', 'and', 'Engr', 'Dept.,', 'Universty', 'of', 'Cal,', 'San', 'Deigo'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego'])