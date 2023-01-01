
# coding=utf-8

from __future__ import unicode_literals

import math
import unittest

from .utils import raises

# sequence based similarity measures
from py_stringmatching.similarity_measure.affine import Affine
from py_stringmatching.similarity_measure.bag_distance import BagDistance
from py_stringmatching.similarity_measure.editex import Editex
from py_stringmatching.similarity_measure.hamming_distance import HammingDistance
from py_stringmatching.similarity_measure.jaro import Jaro
from py_stringmatching.similarity_measure.jaro_winkler import JaroWinkler
from py_stringmatching.similarity_measure.levenshtein import Levenshtein
from py_stringmatching.similarity_measure.needleman_wunsch import NeedlemanWunsch
from py_stringmatching.similarity_measure.smith_waterman import SmithWaterman
# token based similarity measures
from py_stringmatching.similarity_measure.cosine import Cosine
from py_stringmatching.similarity_measure.dice import Dice
from py_stringmatching.similarity_measure.jaccard import Jaccard
from py_stringmatching.similarity_measure.overlap_coefficient import OverlapCoefficient
from py_stringmatching.similarity_measure.soft_tfidf import SoftTfIdf
from py_stringmatching.similarity_measure.tfidf import TfIdf
from py_stringmatching.similarity_measure.tversky_index import TverskyIndex
# hybrid similarity measures
from py_stringmatching.similarity_measure.generalized_jaccard import GeneralizedJaccard
from py_stringmatching.similarity_measure.monge_elkan import MongeElkan
#phonetic similarity measures
from py_stringmatching.similarity_measure.soundex import Soundex
#fuzzywuzzy similarity measures
from py_stringmatching.similarity_measure.partial_ratio import PartialRatio
from py_stringmatching.similarity_measure.ratio import Ratio
from py_stringmatching.similarity_measure.partial_token_sort import PartialTokenSort
from py_stringmatching.similarity_measure.token_sort import TokenSort

NUMBER_OF_DECIMAL_PLACES = 5

# ---------------------- sequence based similarity measures  ----------------------


class AffineTestCases(unittest.TestCase):
    def setUp(self):
        self.affine = Affine()
        self.affine_with_params1 = Affine(gap_start=2, gap_continuation=0.5)
        self.sim_func = lambda s1, s2: (int(1 if s1 == s2 else 0))
        self.affine_with_params2 = Affine(gap_continuation=0.2, sim_func=self.sim_func)

    def test_valid_input(self):
        self.assertAlmostEqual(self.affine.get_raw_score('dva', 'deeva'), 1.5)
        self.assertAlmostEqual(self.affine_with_params1.get_raw_score('dva', 'deeve'), -0.5)
        self.assertAlmostEqual(round(self.affine_with_params2.get_raw_score('AAAGAATTCA',
                                                                            'AAATCA'),NUMBER_OF_DECIMAL_PLACES), 4.4)
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


class BagDistanceTestCases(unittest.TestCase):
    def setUp(self):
        self.bd = BagDistance()

    def test_valid_input_raw_score(self):
        self.assertEqual(self.bd.get_raw_score('a', ''), 1)
        self.assertEqual(self.bd.get_raw_score('', 'a'), 1)
        self.assertEqual(self.bd.get_raw_score('abc', ''), 3)
        self.assertEqual(self.bd.get_raw_score('', 'abc'), 3)
        self.assertEqual(self.bd.get_raw_score('', ''), 0)
        self.assertEqual(self.bd.get_raw_score('a', 'a'), 0)
        self.assertEqual(self.bd.get_raw_score('abc', 'abc'), 0)
        self.assertEqual(self.bd.get_raw_score('a', 'ab'), 1)
        self.assertEqual(self.bd.get_raw_score('b', 'ab'), 1)
        self.assertEqual(self.bd.get_raw_score('ac', 'abc'), 1)
        self.assertEqual(self.bd.get_raw_score('abcdefg', 'xabxcdxxefxgx'), 6)
        self.assertEqual(self.bd.get_raw_score('ab', 'a'), 1)
        self.assertEqual(self.bd.get_raw_score('ab', 'b'), 1)
        self.assertEqual(self.bd.get_raw_score('abc', 'ac'), 1)
        self.assertEqual(self.bd.get_raw_score('xabxcdxxefxgx', 'abcdefg'), 6)
        self.assertEqual(self.bd.get_raw_score('a', 'b'), 1)
        self.assertEqual(self.bd.get_raw_score('ab', 'ac'), 1)
        self.assertEqual(self.bd.get_raw_score('ac', 'bc'), 1)
        self.assertEqual(self.bd.get_raw_score('abc', 'axc'), 1)
        self.assertEqual(self.bd.get_raw_score('xabxcdxxefxgx', '1ab2cd34ef5g6'), 6)
        self.assertEqual(self.bd.get_raw_score('example', 'samples'), 2)
        self.assertEqual(self.bd.get_raw_score('sturgeon', 'urgently'), 2)
        self.assertEqual(self.bd.get_raw_score('bag_distance', 'frankenstein'), 6)
        self.assertEqual(self.bd.get_raw_score('distance', 'difference'), 5)
        self.assertEqual(self.bd.get_raw_score('java was neat', 'scala is great'), 6)

    def test_valid_input_sim_score(self):
        self.assertEqual(self.bd.get_sim_score('a', ''), 0.0)
        self.assertEqual(self.bd.get_sim_score('', 'a'), 0.0)
        self.assertEqual(self.bd.get_sim_score('abc', ''), 0.0)
        self.assertEqual(self.bd.get_sim_score('', 'abc'), 0.0)
        self.assertEqual(self.bd.get_sim_score('', ''), 1.0)
        self.assertEqual(self.bd.get_sim_score('a', 'a'), 1.0)
        self.assertEqual(self.bd.get_sim_score('abc', 'abc'), 1.0)
        self.assertEqual(self.bd.get_sim_score('a', 'ab'), 1.0 - (1.0/2.0))
        self.assertEqual(self.bd.get_sim_score('b', 'ab'), 1.0 - (1.0/2.0))
        self.assertEqual(self.bd.get_sim_score('ac', 'abc'), 1.0 - (1.0/3.0))
        self.assertEqual(self.bd.get_sim_score('abcdefg', 'xabxcdxxefxgx'), 1.0 - (6.0/13.0))
        self.assertEqual(self.bd.get_sim_score('ab', 'a'), 1.0 - (1.0/2.0))
        self.assertEqual(self.bd.get_sim_score('ab', 'b'), 1.0 - (1.0/2.0))
        self.assertEqual(self.bd.get_sim_score('abc', 'ac'), 1.0 - (1.0/3.0))
        self.assertEqual(self.bd.get_sim_score('xabxcdxxefxgx', 'abcdefg'), 1.0 - (6.0/13.0))
        self.assertEqual(self.bd.get_sim_score('a', 'b'), 0.0)
        self.assertEqual(self.bd.get_sim_score('ab', 'ac'), 1.0 - (1.0/2.0))
        self.assertEqual(self.bd.get_sim_score('ac', 'bc'), 1.0 - (1.0/2.0))
        self.assertEqual(self.bd.get_sim_score('abc', 'axc'), 1.0 - (1.0/3.0))
        self.assertEqual(self.bd.get_sim_score('xabxcdxxefxgx', '1ab2cd34ef5g6'), 1.0 - (6.0/13.0))
        self.assertEqual(self.bd.get_sim_score('example', 'samples'), 1.0 - (2.0/7.0))
        self.assertEqual(self.bd.get_sim_score('sturgeon', 'urgently'), 1.0 - (2.0/8.0))
        self.assertEqual(self.bd.get_sim_score('bag_distance', 'frankenstein'), 1.0 - (6.0/12.0))
        self.assertEqual(self.bd.get_sim_score('distance', 'difference'), 1.0 - (5.0/10.0))
        self.assertEqual(self.bd.get_sim_score('java was neat', 'scala is great'), 1.0 - (6.0/14.0))

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.bd.get_raw_score('a', None)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.bd.get_raw_score(None, 'b')

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.bd.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.bd.get_raw_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.bd.get_raw_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.bd.get_raw_score(12.90, 12.90)

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.bd.get_sim_score('a', None)

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.bd.get_sim_score(None, 'b')

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.bd.get_sim_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_sim_score(self):
        self.bd.get_sim_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_sim_score(self):
        self.bd.get_sim_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_sim_score(self):
        self.bd.get_sim_score(12.90, 12.90)


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


class JaroWinklerTestCases(unittest.TestCase):
    def setUp(self):
        self.jw = JaroWinkler()

    def test_get_prefix_weight(self):
        self.assertEqual(self.jw.get_prefix_weight(), 0.1)

    def test_set_prefix_weight(self):
        jw = JaroWinkler(prefix_weight=0.15)
        self.assertEqual(jw.get_prefix_weight(), 0.15)
        self.assertAlmostEqual(jw.get_raw_score('MARTHA', 'MARHTA'), 0.9694444444444444)
        self.assertEqual(jw.set_prefix_weight(0.25), True)
        self.assertEqual(jw.get_prefix_weight(), 0.25)
        self.assertAlmostEqual(jw.get_raw_score('MARTHA', 'MARHTA'), 0.9861111111111112)

    def test_valid_input_raw_score(self):
        # https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance
        self.assertAlmostEqual(self.jw.get_raw_score('MARTHA', 'MARHTA'),
                               0.9611111111111111)
        self.assertAlmostEqual(self.jw.get_raw_score('DWAYNE', 'DUANE'), 0.84)
        self.assertAlmostEqual(self.jw.get_raw_score('DIXON', 'DICKSONX'),
                               0.8133333333333332)

    def test_valid_input_sim_score(self):
        self.assertAlmostEqual(self.jw.get_sim_score('MARTHA', 'MARHTA'),
                               0.9611111111111111)
        self.assertAlmostEqual(self.jw.get_sim_score('DWAYNE', 'DUANE'), 0.84)
        self.assertAlmostEqual(self.jw.get_sim_score('DIXON', 'DICKSONX'),
                               0.8133333333333332)

    def test_non_ascii_input_raw_score(self):
        self.assertAlmostEqual(self.jw.get_raw_score(u'MARTHA', u'MARHTA'),
                               0.9611111111111111)
        self.assertAlmostEqual(self.jw.get_raw_score(u'László', u'Lsáló'),
                               0.8900000000000001)
        self.assertAlmostEqual(self.jw.get_raw_score('László', 'Lsáló'),
                               0.8900000000000001)
        self.assertAlmostEqual(self.jw.get_raw_score(b'L\xc3\xa1szl\xc3\xb3',
                                                     b'Ls\xc3\xa1l\xc3\xb3'),
                               0.8900000000000001)

    def test_non_ascii_input_sim_score(self):
        self.assertAlmostEqual(self.jw.get_sim_score(u'MARTHA', u'MARHTA'),
                               0.9611111111111111)
        self.assertAlmostEqual(self.jw.get_sim_score(u'László', u'Lsáló'),
                               0.8900000000000001)
        self.assertAlmostEqual(self.jw.get_sim_score('László', 'Lsáló'),
                               0.8900000000000001)
        self.assertAlmostEqual(self.jw.get_sim_score(b'L\xc3\xa1szl\xc3\xb3',
                                                     b'Ls\xc3\xa1l\xc3\xb3'),
                               0.8900000000000001)

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.jw.get_raw_score(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.jw.get_raw_score('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.jw.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.jw.get_raw_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.jw.get_raw_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.jw.get_raw_score(12.90, 12.90)

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.jw.get_sim_score(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.jw.get_sim_score('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.jw.get_sim_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_sim_score(self):
        self.jw.get_sim_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_sim_score(self):
        self.jw.get_sim_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_sim_score(self):
        self.jw.get_sim_score(12.90, 12.90)


class LevenshteinTestCases(unittest.TestCase):
    def setUp(self):
        self.lev = Levenshtein()

    def test_valid_input_raw_score(self):
        # http://oldfashionedsoftware.com/tag/levenshtein-distance/
        self.assertEqual(self.lev.get_raw_score('a', ''), 1)
        self.assertEqual(self.lev.get_raw_score('', 'a'), 1)
        self.assertEqual(self.lev.get_raw_score('abc', ''), 3)
        self.assertEqual(self.lev.get_raw_score('', 'abc'), 3)
        self.assertEqual(self.lev.get_raw_score('', ''), 0)
        self.assertEqual(self.lev.get_raw_score('a', 'a'), 0)
        self.assertEqual(self.lev.get_raw_score('abc', 'abc'), 0)
        self.assertEqual(self.lev.get_raw_score('a', 'ab'), 1)
        self.assertEqual(self.lev.get_raw_score('b', 'ab'), 1)
        self.assertEqual(self.lev.get_raw_score('ac', 'abc'), 1)
        self.assertEqual(self.lev.get_raw_score('abcdefg', 'xabxcdxxefxgx'), 6)
        self.assertEqual(self.lev.get_raw_score('ab', 'a'), 1)
        self.assertEqual(self.lev.get_raw_score('ab', 'b'), 1)
        self.assertEqual(self.lev.get_raw_score('abc', 'ac'), 1)
        self.assertEqual(self.lev.get_raw_score('xabxcdxxefxgx', 'abcdefg'), 6)
        self.assertEqual(self.lev.get_raw_score('a', 'b'), 1)
        self.assertEqual(self.lev.get_raw_score('ab', 'ac'), 1)
        self.assertEqual(self.lev.get_raw_score('ac', 'bc'), 1)
        self.assertEqual(self.lev.get_raw_score('abc', 'axc'), 1)
        self.assertEqual(self.lev.get_raw_score('xabxcdxxefxgx', '1ab2cd34ef5g6'), 6)
        self.assertEqual(self.lev.get_raw_score('example', 'samples'), 3)
        self.assertEqual(self.lev.get_raw_score('sturgeon', 'urgently'), 6)
        self.assertEqual(self.lev.get_raw_score('levenshtein', 'frankenstein'), 6)
        self.assertEqual(self.lev.get_raw_score('distance', 'difference'), 5)
        self.assertEqual(self.lev.get_raw_score('java was neat', 'scala is great'), 7)

    def test_valid_input_sim_score(self):
        self.assertEqual(self.lev.get_sim_score('a', ''), 1.0 - (1.0/1.0))
        self.assertEqual(self.lev.get_sim_score('', 'a'), 1.0 - (1.0/1.0))
        self.assertEqual(self.lev.get_sim_score('abc', ''), 1.0 - (3.0/3.0))
        self.assertEqual(self.lev.get_sim_score('', 'abc'), 1.0 - (3.0/3.0))
        self.assertEqual(self.lev.get_sim_score('', ''), 1.0)
        self.assertEqual(self.lev.get_sim_score('a', 'a'), 1.0)
        self.assertEqual(self.lev.get_sim_score('abc', 'abc'), 1.0)
        self.assertEqual(self.lev.get_sim_score('a', 'ab'), 1.0 - (1.0/2.0))
        self.assertEqual(self.lev.get_sim_score('b', 'ab'), 1.0 - (1.0/2.0))
        self.assertEqual(self.lev.get_sim_score('ac', 'abc'), 1.0 - (1.0/3.0))
        self.assertEqual(self.lev.get_sim_score('abcdefg', 'xabxcdxxefxgx'), 1.0 - (6.0/13.0))
        self.assertEqual(self.lev.get_sim_score('ab', 'a'), 1.0 - (1.0/2.0))
        self.assertEqual(self.lev.get_sim_score('ab', 'b'), 1.0 - (1.0/2.0))
        self.assertEqual(self.lev.get_sim_score('abc', 'ac'), 1.0 - (1.0/3.0))
        self.assertEqual(self.lev.get_sim_score('xabxcdxxefxgx', 'abcdefg'), 1.0 - (6.0/13.0))
        self.assertEqual(self.lev.get_sim_score('a', 'b'), 1.0 - (1.0/1.0))
        self.assertEqual(self.lev.get_sim_score('ab', 'ac'), 1.0 - (1.0/2.0))
        self.assertEqual(self.lev.get_sim_score('ac', 'bc'), 1.0 - (1.0/2.0))
        self.assertEqual(self.lev.get_sim_score('abc', 'axc'), 1.0 - (1.0/3.0))
        self.assertEqual(self.lev.get_sim_score('xabxcdxxefxgx', '1ab2cd34ef5g6'), 1.0 - (6.0/13.0))
        self.assertEqual(self.lev.get_sim_score('example', 'samples'), 1.0 - (3.0/7.0))
        self.assertEqual(self.lev.get_sim_score('sturgeon', 'urgently'), 1.0 - (6.0/8.0))
        self.assertEqual(self.lev.get_sim_score('levenshtein', 'frankenstein'), 1.0 - (6.0/12.0))
        self.assertEqual(self.lev.get_sim_score('distance', 'difference'), 1.0 - (5.0/10.0))
        self.assertEqual(self.lev.get_sim_score('java was neat', 'scala is great'),
                         1.0 - (7.0/14.0))

    def test_valid_input_non_ascii_raw_score(self):
        self.assertEqual(self.lev.get_raw_score('ác', 'áóc'), 1)
        self.assertEqual(self.lev.get_raw_score(u'ác', u'áóc'), 1)
        self.assertEqual(self.lev.get_raw_score(b'\xc3\xa1c', b'\xc3\xa1\xc3\xb3c'), 1)

    def test_valid_input_non_ascii_sim_score(self):
        self.assertEqual(self.lev.get_sim_score('ác', 'áóc'), 1.0 - (1.0/3.0))
        self.assertEqual(self.lev.get_sim_score(u'ác', u'áóc'),
                         1.0 - (1.0/3.0))
        self.assertEqual(self.lev.get_sim_score(b'\xc3\xa1c',
                                                b'\xc3\xa1\xc3\xb3c'), 1.0 - (1.0/3.0))

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.lev.get_raw_score('a', None)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.lev.get_raw_score(None, 'b')

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.lev.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.lev.get_raw_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.lev.get_raw_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.lev.get_raw_score(12.90, 12.90)

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.lev.get_sim_score('a', None)

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.lev.get_sim_score(None, 'b')

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.lev.get_sim_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_sim_score(self):
        self.lev.get_sim_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_sim_score(self):
        self.lev.get_sim_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_sim_score(self):
        self.lev.get_sim_score(12.90, 12.90)


class HammingDistanceTestCases(unittest.TestCase):
    def setUp(self):
        self.hd = HammingDistance()

    def test_valid_input_raw_score(self):
        self.assertEqual(self.hd.get_raw_score('-789', 'john'), 4)
        self.assertEqual(self.hd.get_raw_score('a', '*'), 1)
        self.assertEqual(self.hd.get_raw_score('b', 'a'), 1)
        self.assertEqual(self.hd.get_raw_score('abc', 'p q'), 3)
        self.assertEqual(self.hd.get_raw_score('karolin', 'kathrin'), 3)
        self.assertEqual(self.hd.get_raw_score('KARI', 'kari'), 4)
        self.assertEqual(self.hd.get_raw_score('', ''), 0)

    def test_valid_input_sim_score(self):
        self.assertEqual(self.hd.get_sim_score('-789', 'john'), 1.0 - (4.0/4.0))
        self.assertEqual(self.hd.get_sim_score('a', '*'), 1.0 - (1.0/1.0))
        self.assertEqual(self.hd.get_sim_score('b', 'a'), 1.0 - (1.0/1.0))
        self.assertEqual(self.hd.get_sim_score('abc', 'p q'), 1.0 - (3.0/3.0))
        self.assertEqual(self.hd.get_sim_score('karolin', 'kathrin'), 1.0 - (3.0/7.0))
        self.assertEqual(self.hd.get_sim_score('KARI', 'kari'), 1.0 - (4.0/4.0))
        self.assertEqual(self.hd.get_sim_score('', ''), 1.0)

    def test_valid_input_compatibility_raw_score(self):
        self.assertEqual(self.hd.get_raw_score(u'karolin', u'kathrin'), 3)
        self.assertEqual(self.hd.get_raw_score(u'', u''), 0)
        # str_1 = u'foo'.encode(encoding='UTF-8', errors='strict')
        # str_2 = u'bar'.encode(encoding='UTF-8', errors='strict')
        # self.assertEqual(self.hd.get_raw_score(str_1, str_2), 3) # check with Ali - python 3 returns type error
        # self.assertEqual(self.hd.get_raw_score(str_1, str_1), 0) # check with Ali - python 3 returns type error

    def test_valid_input_compatibility_sim_score(self):
        self.assertEqual(self.hd.get_sim_score(u'karolin', u'kathrin'), 1.0 - (3.0/7.0))
        self.assertEqual(self.hd.get_sim_score(u'', u''), 1.0)

    def test_valid_input_non_ascii_raw_score(self):
        self.assertEqual(self.hd.get_raw_score(u'ábó', u'áóó'), 1)
        self.assertEqual(self.hd.get_raw_score('ábó', 'áóó'), 1)
        self.assertEqual(self.hd.get_raw_score(b'\xc3\xa1b\xc3\xb3',
                                               b'\xc3\xa1\xc3\xb3\xc3\xb3'),
                         1)

    def test_valid_input_non_ascii_sim_score(self):
        self.assertEqual(self.hd.get_sim_score(u'ábó', u'áóó'), 1.0 - (1.0/3.0))
        self.assertEqual(self.hd.get_sim_score('ábó', 'áóó'), 1.0 - (1.0/3.0))
        self.assertEqual(self.hd.get_sim_score(b'\xc3\xa1b\xc3\xb3',
                                               b'\xc3\xa1\xc3\xb3\xc3\xb3'),
                         1.0 - (1.0/3.0))

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.hd.get_raw_score('a', None)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.hd.get_raw_score(None, 'b')

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.hd.get_raw_score(None, None)

    @raises(ValueError)
    def test_invalid_input4_raw_score(self):
        self.hd.get_raw_score('a', '')

    @raises(ValueError)
    def test_invalid_input5_raw_score(self):
        self.hd.get_raw_score('', 'This is a long string')

    @raises(ValueError)
    def test_invalid_input6_raw_score(self):
        self.hd.get_raw_score('ali', 'alex')

    @raises(TypeError)
    def test_invalid_input7_raw_score(self):
        self.hd.get_raw_score('MA', 12)

    @raises(TypeError)
    def test_invalid_input8_raw_score(self):
        self.hd.get_raw_score(12, 'MA')

    @raises(TypeError)
    def test_invalid_input9_raw_score(self):
        self.hd.get_raw_score(12, 12)

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.hd.get_sim_score('a', None)

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.hd.get_sim_score(None, 'b')

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.hd.get_sim_score(None, None)

    @raises(ValueError)
    def test_invalid_input4_sim_score(self):
        self.hd.get_sim_score('a', '')

    @raises(ValueError)
    def test_invalid_input5_sim_score(self):
        self.hd.get_sim_score('', 'This is a long string')

    @raises(ValueError)
    def test_invalid_input6_sim_score(self):
        self.hd.get_sim_score('ali', 'alex')

    @raises(TypeError)
    def test_invalid_input7_sim_score(self):
        self.hd.get_sim_score('MA', 12)

    @raises(TypeError)
    def test_invalid_input8_sim_score(self):
        self.hd.get_sim_score(12, 'MA')

    @raises(TypeError)
    def test_invalid_input9_sim_score(self):
        self.hd.get_sim_score(12, 12)


class NeedlemanWunschTestCases(unittest.TestCase):
    def setUp(self):
        self.nw = NeedlemanWunsch()
        self.nw_with_params1 = NeedlemanWunsch(0.0)
        self.nw_with_params2 = NeedlemanWunsch(1.0, sim_func=lambda s1, s2: (2 if s1 == s2 else -1))
        self.sim_func = lambda s1, s2: (1 if s1 == s2 else -1)
        self.nw_with_params3 = NeedlemanWunsch(gap_cost=0.5, sim_func=self.sim_func)

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


class SmithWatermanTestCases(unittest.TestCase):
    def setUp(self):
        self.sw = SmithWaterman()
        self.sw_with_params1 = SmithWaterman(2.2)
        self.sw_with_params2 = SmithWaterman(1, sim_func=lambda s1, s2:(2 if s1 == s2 else -1))
        self.sw_with_params3 = SmithWaterman(gap_cost=1, sim_func=lambda s1, s2:(int(1 if s1 == s2 else -1)))
        self.sim_func = lambda s1, s2: (1.5 if s1 == s2 else 0.5)
        self.sw_with_params4 = SmithWaterman(gap_cost=1.4, sim_func=self.sim_func)

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


class SoundexTestCases(unittest.TestCase):
    def setUp(self):
        self.sdx = Soundex()

    def test_valid_input_raw_score(self):
        self.assertEqual(self.sdx.get_raw_score('Robert', 'Rupert'), 1)
        self.assertEqual(self.sdx.get_raw_score('Sue', 'S'), 1)
        self.assertEqual(self.sdx.get_raw_score('robert', 'rupert'), 1)
        self.assertEqual(self.sdx.get_raw_score('Gough', 'goff'), 0)
        self.assertEqual(self.sdx.get_raw_score('gough', 'Goff'), 0)
        self.assertEqual(self.sdx.get_raw_score('ali', 'a,,,li'), 1)
        self.assertEqual(self.sdx.get_raw_score('Jawornicki', 'Yavornitzky'), 0)
        self.assertEqual(self.sdx.get_raw_score('Robert', 'Robert'), 1)

    def test_valid_input_sim_score(self):
        self.assertEqual(self.sdx.get_sim_score('Robert', 'Rupert'), 1)
        self.assertEqual(self.sdx.get_sim_score('Sue', 'S'), 1)
        self.assertEqual(self.sdx.get_sim_score('robert', 'rupert'), 1)
        self.assertEqual(self.sdx.get_sim_score('Gough', 'goff'), 0)
        self.assertEqual(self.sdx.get_sim_score('gough', 'Goff'), 0)
        self.assertEqual(self.sdx.get_sim_score('ali', 'a,,,li'), 1)
        self.assertEqual(self.sdx.get_sim_score('Jawornicki', 'Yavornitzky'), 0)
        self.assertEqual(self.sdx.get_sim_score('Robert', 'Robert'), 1)

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.sdx.get_raw_score('a', None)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.sdx.get_raw_score(None, 'b')

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.sdx.get_raw_score(None, None)

    @raises(ValueError)
    def test_invalid_input4_raw_score(self):
        self.sdx.get_raw_score('a', '')

    @raises(ValueError)
    def test_invalid_input5_raw_score(self):
        self.sdx.get_raw_score('', 'This is a long string')

    @raises(TypeError)
    def test_invalid_input7_raw_score(self):
        self.sdx.get_raw_score('xyz', [''])

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.sdx.get_sim_score('a', None)

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.sdx.get_sim_score(None, 'b')

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.sdx.get_sim_score(None, None)

    @raises(ValueError)
    def test_invalid_input4_sim_score(self):
        self.sdx.get_sim_score('a', '')

    @raises(ValueError)
    def test_invalid_input5_sim_score(self):
        self.sdx.get_sim_score('', 'This is a long string')

    @raises(TypeError)
    def test_invalid_input7_sim_score(self):
        self.sdx.get_sim_score('xyz', [''])


# ---------------------- token based similarity measures  ----------------------

# ---------------------- set based similarity measures  ----------------------
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


class DiceTestCases(unittest.TestCase):
    def setUp(self):
        self.dice = Dice()

    def test_valid_input_raw_score(self):
        self.assertEqual(self.dice.get_raw_score(['data', 'science'], ['data']),
                         2 * 1.0 / 3.0)
        self.assertEqual(self.dice.get_raw_score(['data', 'science'], ['science', 'good']),
                         2 * 1.0 / 4.0)
        self.assertEqual(self.dice.get_raw_score([], ['data']), 0)
        self.assertEqual(self.dice.get_raw_score(['data', 'data', 'science'],
                                                 ['data', 'management']), 2 * 1.0 / 4.0)
        self.assertEqual(self.dice.get_raw_score(['data', 'management'],
                                                 ['data', 'data', 'science']), 2 * 1.0 / 4.0)
        self.assertEqual(self.dice.get_raw_score([], []), 1.0)
        self.assertEqual(self.dice.get_raw_score(['a', 'b'], ['b', 'a']), 1.0)
        self.assertEqual(self.dice.get_raw_score(set([]), set([])), 1.0)
        self.assertEqual(self.dice.get_raw_score({1, 1, 2, 3, 4}, {2, 3, 4, 5, 6, 7, 7, 8}),
                         2 * 3.0 / 11.0)

    def test_valid_input_sim_score(self):
        self.assertEqual(self.dice.get_sim_score(['data', 'science'], ['data']),
                         2 * 1.0 / 3.0)
        self.assertEqual(self.dice.get_sim_score(['data', 'science'], ['science', 'good']),
                         2 * 1.0 / 4.0)
        self.assertEqual(self.dice.get_sim_score([], ['data']), 0)
        self.assertEqual(self.dice.get_sim_score(['data', 'data', 'science'],
                                                 ['data', 'management']), 2 * 1.0 / 4.0)
        self.assertEqual(self.dice.get_sim_score(['data', 'management'],
                                                 ['data', 'data', 'science']), 2 * 1.0 / 4.0)
        self.assertEqual(self.dice.get_sim_score([], []), 1.0)
        self.assertEqual(self.dice.get_sim_score(['a', 'b'], ['b', 'a']), 1.0)
        self.assertEqual(self.dice.get_sim_score(set([]), set([])), 1.0)
        self.assertEqual(self.dice.get_sim_score({1, 1, 2, 3, 4}, {2, 3, 4, 5, 6, 7, 7, 8}),
                         2 * 3.0 / 11.0)

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.dice.get_raw_score(1, 1)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.dice.get_raw_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.dice.get_raw_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.dice.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.dice.get_raw_score(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.dice.get_raw_score('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input7_raw_score(self):
        self.dice.get_raw_score('MARHTA', 'MARTHA')

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.dice.get_sim_score(1, 1)

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.dice.get_sim_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.dice.get_sim_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input4_sim_score(self):
        self.dice.get_sim_score(None, None)

    @raises(TypeError)
    def test_invalid_input5_sim_score(self):
        self.dice.get_sim_score(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input6_sim_score(self):
        self.dice.get_sim_score('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input7_sim_score(self):
        self.dice.get_sim_score('MARHTA', 'MARTHA')


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
        self.assertEqual(self.jac.get_raw_score(set([]),
                                                set([])), 1.0)
        self.assertEqual(self.jac.get_raw_score({1, 1, 2, 3, 4}, {2, 3, 4, 5, 6, 7, 7, 8}), 3.0 / 8.0)

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


# Modified test cases to overcome the decimal points matching
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
        self.assertAlmostEqual(round(gj.get_raw_score(['Niall'], ['Neal', 'Njall']), NUMBER_OF_DECIMAL_PLACES),
                               round(0.43333333333333335, NUMBER_OF_DECIMAL_PLACES))
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
        self.assertAlmostEqual(round(gj.get_raw_score(['Niall'], ['Neal', 'Njall']), NUMBER_OF_DECIMAL_PLACES),
                               round(0.43333333333333335, NUMBER_OF_DECIMAL_PLACES))

    def test_valid_input_raw_score(self):
        self.assertEqual(self.gen_jac.get_raw_score([''], ['']), 1.0)  # need to check this

        self.assertEqual(self.gen_jac.get_raw_score([''], ['a']), 0.0)
        self.assertEqual(self.gen_jac.get_raw_score(['a'], ['a']), 1.0)

        self.assertEqual(self.gen_jac.get_raw_score([], ['Nigel']), 0.0)
        self.assertEqual(round(self.gen_jac.get_raw_score(['Niall'], ['Neal']), NUMBER_OF_DECIMAL_PLACES),
                         round(0.7833333333333333, NUMBER_OF_DECIMAL_PLACES))
        self.assertEqual(round(self.gen_jac.get_raw_score(['Niall'], ['Njall', 'Neal']), NUMBER_OF_DECIMAL_PLACES),
                         round(0.43333333333333335, NUMBER_OF_DECIMAL_PLACES))
        self.assertEqual(round(self.gen_jac.get_raw_score(['Niall'], ['Neal', 'Njall']), NUMBER_OF_DECIMAL_PLACES),
                         round(0.43333333333333335, NUMBER_OF_DECIMAL_PLACES))
        self.assertEqual(round(self.gen_jac.get_raw_score(
                ['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            NUMBER_OF_DECIMAL_PLACES), round(0.6800468975468975, NUMBER_OF_DECIMAL_PLACES))

        self.assertEqual(round(self.gen_jac_with_jw.get_raw_score(
                ['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            NUMBER_OF_DECIMAL_PLACES), round(0.7220003607503608, NUMBER_OF_DECIMAL_PLACES ))
        self.assertEqual(round(self.gen_jac_with_jw.get_raw_score(
                ['Comp', 'Sci.', 'and', 'Engr', 'Dept.,', 'Universty', 'of', 'Cal,', 'San', 'Deigo'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            NUMBER_OF_DECIMAL_PLACES), round(0.7075277777777778, NUMBER_OF_DECIMAL_PLACES))

        self.assertEqual(round(self.gen_jac_with_jw_08.get_raw_score(
                ['Comp', 'Sci.', 'and', 'Engr', 'Dept.,', 'Universty', 'of', 'Cal,', 'San', 'Deigo'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            NUMBER_OF_DECIMAL_PLACES), round(0.45810185185185187, NUMBER_OF_DECIMAL_PLACES))

    def test_valid_input_sim_score(self):
        self.assertEqual(self.gen_jac.get_sim_score([''], ['']), 1.0)  # need to check this

        self.assertEqual(self.gen_jac.get_sim_score([''], ['a']), 0.0)
        self.assertEqual(self.gen_jac.get_sim_score(['a'], ['a']), 1.0)

        self.assertEqual(self.gen_jac.get_sim_score([], ['Nigel']), 0.0)
        self.assertEqual(round(self.gen_jac.get_sim_score(['Niall'], ['Neal']), NUMBER_OF_DECIMAL_PLACES),
                         round(0.7833333333333333, NUMBER_OF_DECIMAL_PLACES))
        self.assertEqual(round(self.gen_jac.get_sim_score(['Niall'], ['Njall', 'Neal']), NUMBER_OF_DECIMAL_PLACES),
                         round(0.43333333333333335, NUMBER_OF_DECIMAL_PLACES))
        self.assertEqual(round(self.gen_jac.get_sim_score(['Niall'], ['Neal', 'Njall']), NUMBER_OF_DECIMAL_PLACES),
                         round(0.43333333333333335, NUMBER_OF_DECIMAL_PLACES))
        self.assertEqual(round(self.gen_jac.get_sim_score(
                ['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            NUMBER_OF_DECIMAL_PLACES), round(0.6800468975468975, NUMBER_OF_DECIMAL_PLACES))

        self.assertEqual(round(self.gen_jac_with_jw.get_sim_score(
                ['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            NUMBER_OF_DECIMAL_PLACES),round(0.7220003607503608, NUMBER_OF_DECIMAL_PLACES))
        self.assertEqual(round(self.gen_jac_with_jw.get_sim_score(
                ['Comp', 'Sci.', 'and', 'Engr', 'Dept.,', 'Universty', 'of', 'Cal,', 'San', 'Deigo'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            NUMBER_OF_DECIMAL_PLACES), round(0.7075277777777778, NUMBER_OF_DECIMAL_PLACES))

        self.assertEqual(round(self.gen_jac_with_jw_08.get_sim_score(
                ['Comp', 'Sci.', 'and', 'Engr', 'Dept.,', 'Universty', 'of', 'Cal,', 'San', 'Deigo'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            NUMBER_OF_DECIMAL_PLACES), round(0.45810185185185187, NUMBER_OF_DECIMAL_PLACES))

    def test_valid_input_non_ascii_raw_score(self):
        self.assertEqual(round(self.gen_jac.get_raw_score([u'Nóáll'], [u'Neál']), NUMBER_OF_DECIMAL_PLACES),
                         round(0.7833333333333333, NUMBER_OF_DECIMAL_PLACES))
        self.assertEqual(round(self.gen_jac.get_raw_score(['Nóáll'], ['Neál']), NUMBER_OF_DECIMAL_PLACES),
                         round(0.7833333333333333, NUMBER_OF_DECIMAL_PLACES))
        self.assertEqual(round(self.gen_jac.get_raw_score([b'N\xc3\xb3\xc3\xa1ll'], [b'Ne\xc3\xa1l']),
                               NUMBER_OF_DECIMAL_PLACES), round(0.7833333333333333, NUMBER_OF_DECIMAL_PLACES))

    def test_valid_input_non_ascii_sim_score(self):
        self.assertEqual(round(self.gen_jac.get_sim_score([u'Nóáll'], [u'Neál']), NUMBER_OF_DECIMAL_PLACES),
                          round(0.7833333333333333, NUMBER_OF_DECIMAL_PLACES))
        self.assertEqual(round(self.gen_jac.get_sim_score(['Nóáll'], ['Neál']), NUMBER_OF_DECIMAL_PLACES),
                         round(0.7833333333333333, NUMBER_OF_DECIMAL_PLACES))
        self.assertEqual(round(self.gen_jac.get_sim_score([b'N\xc3\xb3\xc3\xa1ll'], [b'Ne\xc3\xa1l']),
                               NUMBER_OF_DECIMAL_PLACES), round(0.7833333333333333, NUMBER_OF_DECIMAL_PLACES))

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


class CosineTestCases(unittest.TestCase):
    def setUp(self):
        self.cos = Cosine()

    def test_valid_input_raw_score(self):
        self.assertEqual(self.cos.get_raw_score(['data', 'science'], ['data']), 1.0 / (math.sqrt(2) * math.sqrt(1)))
        self.assertEqual(self.cos.get_raw_score(['data', 'science'], ['science', 'good']),
                         1.0 / (math.sqrt(2) * math.sqrt(2)))
        self.assertEqual(self.cos.get_raw_score([], ['data']), 0.0)
        self.assertEqual(self.cos.get_raw_score(['data', 'data', 'science'], ['data', 'management']),
                         1.0 / (math.sqrt(2) * math.sqrt(2)))
        self.assertEqual(self.cos.get_raw_score(['data', 'management'], ['data', 'data', 'science']),
                         1.0 / (math.sqrt(2) * math.sqrt(2)))
        self.assertEqual(self.cos.get_raw_score([], []), 1.0)
        self.assertEqual(self.cos.get_raw_score(set([]), set([])), 1.0)
        self.assertEqual(self.cos.get_raw_score({1, 1, 2, 3, 4}, {2, 3, 4, 5, 6, 7, 7, 8}),
                         3.0 / (math.sqrt(4) * math.sqrt(7)))

    def test_valid_input_sim_score(self):
        self.assertEqual(self.cos.get_sim_score(['data', 'science'], ['data']), 1.0 / (math.sqrt(2) * math.sqrt(1)))
        self.assertEqual(self.cos.get_sim_score(['data', 'science'], ['science', 'good']),
                         1.0 / (math.sqrt(2) * math.sqrt(2)))
        self.assertEqual(self.cos.get_sim_score([], ['data']), 0.0)
        self.assertEqual(self.cos.get_sim_score(['data', 'data', 'science'], ['data', 'management']),
                         1.0 / (math.sqrt(2) * math.sqrt(2)))
        self.assertEqual(self.cos.get_sim_score(['data', 'management'], ['data', 'data', 'science']),
                         1.0 / (math.sqrt(2) * math.sqrt(2)))
        self.assertEqual(self.cos.get_sim_score([], []), 1.0)
        self.assertEqual(self.cos.get_sim_score(set([]), set([])), 1.0)
        self.assertEqual(self.cos.get_sim_score({1, 1, 2, 3, 4}, {2, 3, 4, 5, 6, 7, 7, 8}),
                         3.0 / (math.sqrt(4) * math.sqrt(7)))

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.cos.get_raw_score(1, 1)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.cos.get_raw_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.cos.get_raw_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.cos.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.cos.get_raw_score(['MARHTA'], 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.cos.get_raw_score('MARHTA', ['MARTHA'])

    @raises(TypeError)
    def test_invalid_input7_raw_score(self):
        self.cos.get_raw_score('MARTHA', 'MARTHA')

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.cos.get_sim_score(1, 1)

    @raises(TypeError)
    def test_invalid_input4_sim_score(self):
        self.cos.get_sim_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.cos.get_sim_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.cos.get_sim_score(None, None)

    @raises(TypeError)
    def test_invalid_input5_sim_score(self):
        self.cos.get_sim_score(['MARHTA'], 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_sim_score(self):
        self.cos.get_sim_score('MARHTA', ['MARTHA'])

    @raises(TypeError)
    def test_invalid_input7_sim_score(self):
        self.cos.get_sim_score('MARTHA', 'MARTHA')


class TfidfTestCases(unittest.TestCase):
    def setUp(self):
        self.tfidf = TfIdf()
        self.corpus = [['a', 'b', 'a'], ['a', 'c'], ['a'], ['b']]
        self.tfidf_with_params1 = TfIdf(self.corpus, True)
        self.tfidf_with_params2 = TfIdf([['a', 'b', 'a'], ['a', 'c'], ['a']])
        self.tfidf_with_params3 = TfIdf([['x', 'y'], ['w'], ['q']])

    def test_get_corpus_list(self):
        self.assertEqual(self.tfidf_with_params1.get_corpus_list(), self.corpus)

    def test_get_dampen(self):
        self.assertEqual(self.tfidf_with_params1.get_dampen(), True)

    def test_set_corpus_list(self):
        corpus1 = [['a', 'b', 'a'], ['a', 'c'], ['a'], ['b']]
        corpus2 = [['a', 'b', 'a'], ['a', 'c'], ['a'], ['b'], ['c', 'a', 'b']]
        tfidf = TfIdf(corpus_list=corpus1)
        self.assertEqual(tfidf.get_corpus_list(), corpus1)
        self.assertAlmostEqual(tfidf.get_raw_score(['a', 'b', 'a'], ['a']), 0.5495722661728765)
        self.assertEqual(tfidf.set_corpus_list(corpus2), True)
        self.assertEqual(tfidf.get_corpus_list(), corpus2)
        self.assertAlmostEqual(tfidf.get_raw_score(['a', 'b', 'a'], ['a']), 0.5692378887901467)

    def test_set_dampen(self):
        tfidf = TfIdf(self.corpus, dampen=False)
        self.assertEqual(tfidf.get_dampen(), False)
        self.assertAlmostEqual(tfidf.get_raw_score(['a', 'b', 'a'], ['a']), 0.7999999999999999)
        self.assertEqual(tfidf.set_dampen(True), True)
        self.assertEqual(tfidf.get_dampen(), True)
        self.assertAlmostEqual(tfidf.get_raw_score(['a', 'b', 'a'], ['a']), 0.5495722661728765)

    def test_valid_input_raw_score(self):
        self.assertEqual(self.tfidf_with_params1.get_raw_score(['a', 'b', 'a'], ['a', 'c']),
                         0.11166746710505392)
        self.assertEqual(self.tfidf_with_params2.get_raw_score(['a', 'b', 'a'], ['a', 'c']),
                         0.0)
        self.assertEqual(self.tfidf_with_params2.get_raw_score(['a', 'b', 'a'], ['a']),
                         0.0)
        self.assertEqual(self.tfidf.get_raw_score(['a', 'b', 'a'], ['a']), 0.0)
        self.assertEqual(self.tfidf_with_params3.get_raw_score(['a', 'b', 'a'], ['a']), 0.0)
        self.assertEqual(self.tfidf.get_raw_score(['a', 'b', 'a'], ['a']), 0.0)
        self.assertEqual(self.tfidf.get_raw_score(['a', 'b', 'a'], ['a', 'b', 'a']), 1.0)
        self.assertEqual(self.tfidf.get_raw_score([], ['a', 'b', 'a']), 0.0)

    def test_valid_input_sim_score(self):
        self.assertEqual(self.tfidf_with_params1.get_sim_score(['a', 'b', 'a'], ['a', 'c']),
                         0.11166746710505392)
        self.assertEqual(self.tfidf_with_params2.get_sim_score(['a', 'b', 'a'], ['a', 'c']),
                         0.0)
        self.assertEqual(self.tfidf_with_params2.get_sim_score(['a', 'b', 'a'], ['a']),
                         0.0)
        self.assertEqual(self.tfidf.get_sim_score(['a', 'b', 'a'], ['a']), 0.0)
        self.assertEqual(self.tfidf_with_params3.get_sim_score(['a', 'b', 'a'], ['a']), 0.0)
        self.assertEqual(self.tfidf.get_sim_score(['a', 'b', 'a'], ['a']), 0.0)
        self.assertEqual(self.tfidf.get_sim_score(['a', 'b', 'a'], ['a', 'b', 'a']), 1.0)
        self.assertEqual(self.tfidf.get_sim_score([], ['a', 'b', 'a']), 0.0)

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.tfidf.get_raw_score(1, 1)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.tfidf.get_raw_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.tfidf.get_raw_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.tfidf.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.tfidf.get_raw_score(['MARHTA'], 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.tfidf.get_raw_score('MARHTA', ['MARTHA'])

    @raises(TypeError)
    def test_invalid_input7_raw_score(self):
        self.tfidf.get_raw_score('MARTHA', 'MARTHA')

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.tfidf.get_sim_score(1, 1)

    @raises(TypeError)
    def test_invalid_input4_sim_score(self):
        self.tfidf.get_sim_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.tfidf.get_sim_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.tfidf.get_sim_score(None, None)

    @raises(TypeError)
    def test_invalid_input5_sim_score(self):
        self.tfidf.get_sim_score(['MARHTA'], 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_sim_score(self):
        self.tfidf.get_sim_score('MARHTA', ['MARTHA'])

    @raises(TypeError)
    def test_invalid_input7_sim_score(self):
        self.tfidf.get_sim_score('MARTHA', 'MARTHA')


class TverskyIndexTestCases(unittest.TestCase):
    def setUp(self):
        self.tvi = TverskyIndex()
        self.tvi_with_params1 = TverskyIndex(0.5, 0.5)
        self.tvi_with_params2 = TverskyIndex(0.7, 0.8)
        self.tvi_with_params3 = TverskyIndex(0.2, 0.4)
        self.tvi_with_params4 = TverskyIndex(0.9, 0.8)
        self.tvi_with_params5 = TverskyIndex(0.45, 0.85)
        self.tvi_with_params6 = TverskyIndex(0, 0.6)

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
        self.assertEqual(self.tvi.get_raw_score(['data'], []), 0)
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
        self.assertEqual(self.tvi_with_params6.get_raw_score(['data', 'science'],
							                                 ['data', 'data', 'management', 'science']),
                         2.0 / (2.0 + 0 + 0.6*1))

    def test_valid_input_sim_score(self):
        self.assertEqual(self.tvi_with_params1.get_sim_score(['data', 'science'], ['data']),
                         1.0 / (1.0 + 0.5*1 + 0.5*0))
        self.assertEqual(self.tvi.get_sim_score(['data', 'science'], ['science', 'good']),
                         1.0 / (1.0 + 0.5*1 + 0.5*1))
        self.assertEqual(self.tvi.get_sim_score([], ['data']), 0)
        self.assertEqual(self.tvi.get_sim_score(['data'], []), 0)
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
        self.assertEqual(self.tvi_with_params6.get_sim_score(['data', 'science'],
                                                             ['data', 'data', 'management', 'science']),
                         2.0 / (2.0 + 0 + 0.6*1))

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


# ---------------------- bag based similarity measures  ----------------------
# class CosineTestCases(unittest.TestCase):
#     def test_valid_input(self):
#         NONQ_FROM = 'The quick brown fox jumped over the lazy dog.'
#         NONQ_TO = 'That brown dog jumped over the fox.'
#         self.assertEqual(cosine([], []), 1) # check-- done. both simmetrics, abydos return 1.
#         self.assertEqual(cosine(['the', 'quick'], []), 0)
#         self.assertEqual(cosine([], ['the', 'quick']), 0)
#         self.assertAlmostEqual(cosine(whitespace(NONQ_TO), whitespace(NONQ_FROM)),
#                                4/math.sqrt(9*7))
#
#     @raises(TypeError)
#     def test_invalid_input1_raw_score(self):
#         cosine(['a'], None)
#     @raises(TypeError)
#     def test_invalid_input2_raw_score(self):
#         cosine(None, ['b'])
#     @raises(TypeError)
#     def test_invalid_input3_raw_score(self):
#         cosine(None, None)


# ---------------------- hybrid similarity measure  ----------------------

class Soft_TfidfTestCases(unittest.TestCase):
    def setUp(self):
        self.soft_tfidf = SoftTfIdf()
        self.corpus = [['a', 'b', 'a'], ['a', 'c'], ['a']]
        self.non_ascii_corpus = [['á', 'b', 'á'], ['á', 'c'], ['á']]
        self.soft_tfidf_with_params1 = SoftTfIdf(self.corpus,
                                                 sim_func=Jaro().get_raw_score,
                                                 threshold=0.8)
        self.soft_tfidf_with_params2 = SoftTfIdf(self.corpus,
                                                 threshold=0.9)
        self.soft_tfidf_with_params3 = SoftTfIdf([['x', 'y'], ['w'], ['q']])
        self.affine_fn = Affine().get_raw_score
        self.soft_tfidf_with_params4 = SoftTfIdf(sim_func=self.affine_fn, threshold=0.6)
        self.soft_tfidf_non_ascii = SoftTfIdf(self.non_ascii_corpus,
                                              sim_func=Jaro().get_raw_score,
                                              threshold=0.8)

    def test_get_corpus_list(self):
        self.assertEqual(self.soft_tfidf_with_params1.get_corpus_list(), self.corpus)

    def test_get_sim_func(self):
        self.assertEqual(self.soft_tfidf_with_params4.get_sim_func(), self.affine_fn)

    def test_get_threshold(self):
        self.assertEqual(self.soft_tfidf_with_params4.get_threshold(), 0.6)

    def test_set_corpus_list(self):
        corpus1 = [['a', 'b', 'a'], ['a', 'c'], ['a'], ['b']]
        corpus2 = [['a', 'b', 'a'], ['a', 'c'], ['a'], ['b'], ['c', 'a', 'b']]
        soft_tfidf = SoftTfIdf(corpus_list=corpus1)
        self.assertEqual(soft_tfidf.get_corpus_list(), corpus1)
        self.assertAlmostEqual(soft_tfidf.get_raw_score(['a', 'b', 'a'], ['a']),
                               0.7999999999999999)
        self.assertEqual(soft_tfidf.set_corpus_list(corpus2), True)
        self.assertEqual(soft_tfidf.get_corpus_list(), corpus2)
        self.assertAlmostEqual(soft_tfidf.get_raw_score(['a', 'b', 'a'], ['a']),
                               0.8320502943378437)

    def test_set_threshold(self):
        soft_tfidf = SoftTfIdf(threshold=0.5)
        self.assertEqual(soft_tfidf.get_threshold(), 0.5)
        self.assertAlmostEqual(soft_tfidf.get_raw_score(['ar', 'bfff', 'ab'], ['abcd']), 0.8179128813519699)
        self.assertEqual(soft_tfidf.set_threshold(0.7), True)
        self.assertEqual(soft_tfidf.get_threshold(), 0.7)
        self.assertAlmostEqual(soft_tfidf.get_raw_score(['ar', 'bfff', 'ab'], ['abcd']), 0.4811252243246882)

    def test_set_sim_func(self):
        fn1 = JaroWinkler().get_raw_score
        fn2 = Jaro().get_raw_score
        soft_tfidf = SoftTfIdf(sim_func=fn1)
        self.assertEqual(soft_tfidf.get_sim_func(), fn1)
        self.assertAlmostEqual(soft_tfidf.get_raw_score(['ar', 'bfff', 'ab'], ['abcd']), 0.8612141515411919)
        self.assertEqual(soft_tfidf.set_sim_func(fn2), True)
        self.assertEqual(soft_tfidf.get_sim_func(), fn2)
        self.assertAlmostEqual(soft_tfidf.get_raw_score(['ar', 'bfff', 'ab'], ['abcd']), 0.8179128813519699)

    def test_valid_input_raw_score(self):
        self.assertEqual(self.soft_tfidf_with_params1.get_raw_score(
                         ['a', 'b', 'a'], ['a', 'c']), 0.17541160386140586)
        self.assertEqual(self.soft_tfidf_with_params2.get_raw_score(
                         ['a', 'b', 'a'], ['a']), 0.5547001962252291)
        self.assertEqual(self.soft_tfidf_with_params3.get_raw_score(
                         ['a', 'b', 'a'], ['a']), 0.0)
        self.assertEqual(self.soft_tfidf_with_params4.get_raw_score(
                             ['aa', 'bb', 'a'], ['ab', 'ba']),
                         0.81649658092772592)
        self.assertEqual(self.soft_tfidf.get_raw_score(
                         ['a', 'b', 'a'], ['a', 'b', 'a']), 1.0)
        self.assertEqual(self.soft_tfidf.get_raw_score([], ['a', 'b', 'a']), 0.0)

    def test_valid_input_non_ascii_raw_score(self):
        self.assertEqual(self.soft_tfidf_non_ascii.get_raw_score(
                         [u'á', u'b', u'á'], [u'á', u'c']), 0.17541160386140586)
        self.assertEqual(self.soft_tfidf_non_ascii.get_raw_score(
                         ['á', 'b', 'á'], ['á', 'c']), 0.17541160386140586)

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.soft_tfidf.get_raw_score(1, 1)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.soft_tfidf.get_raw_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.soft_tfidf.get_raw_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.soft_tfidf.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.soft_tfidf.get_raw_score(['MARHTA'], 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.soft_tfidf.get_raw_score('MARHTA', ['MARTHA'])

    @raises(TypeError)
    def test_invalid_input7_raw_score(self):
        self.soft_tfidf.get_raw_score('MARTHA', 'MARTHA')


# Modified test cases to overcome the decimal points matching
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
        self.assertAlmostEqual(round(me.get_raw_score(
                ['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            NUMBER_OF_DECIMAL_PLACES), round(0.8364448051948052, NUMBER_OF_DECIMAL_PLACES))
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

        self.assertEqual(round(self.me.get_raw_score(['Niall'], ['Neal']), NUMBER_OF_DECIMAL_PLACES),
                         round(0.8049999999999999, NUMBER_OF_DECIMAL_PLACES))
        self.assertEqual(round(self.me.get_raw_score(['Niall'], ['Njall']), NUMBER_OF_DECIMAL_PLACES), 0.88)
        self.assertEqual(round(self.me.get_raw_score(
                ['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            NUMBER_OF_DECIMAL_PLACES), round(0.8364448051948052, NUMBER_OF_DECIMAL_PLACES))
        self.assertEqual(self.me_with_nw.get_raw_score(
                ['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            2.0)
        self.assertEqual(self.me_with_affine.get_raw_score(
                ['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            2.25)
        self.assertEqual(round(self.me.get_raw_score(['Niall'], ['Niel']), NUMBER_OF_DECIMAL_PLACES),
                         round(0.8266666666666667, NUMBER_OF_DECIMAL_PLACES))
        self.assertEqual(round(self.me.get_raw_score(['Niall'], ['Nigel']), NUMBER_OF_DECIMAL_PLACES),
                         round(0.7866666666666667, NUMBER_OF_DECIMAL_PLACES))
        self.assertEqual(self.me.get_raw_score([], ['Nigel']), 0.0)

    def test_valid_input_non_ascii(self):
        self.assertEqual(round(self.me.get_raw_score([u'Nóáll'], [u'Neál']), NUMBER_OF_DECIMAL_PLACES),
                         round(0.8049999999999999, NUMBER_OF_DECIMAL_PLACES))
        self.assertEqual(round(self.me.get_raw_score(['Nóáll'], ['Neál']), NUMBER_OF_DECIMAL_PLACES),
                         round(0.8049999999999999, NUMBER_OF_DECIMAL_PLACES))
        self.assertEqual(round(self.me.get_raw_score([b'N\xc3\xb3\xc3\xa1ll'], [b'Ne\xc3\xa1l']),
                               NUMBER_OF_DECIMAL_PLACES), round(0.8049999999999999, NUMBER_OF_DECIMAL_PLACES))

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

# ---------------------- fuzzywuzzy similarity measure  ----------------------

class PartialRatioTestCases(unittest.TestCase):
    def setUp(self):
        self.ratio = PartialRatio()

    def test_valid_input_raw_score(self):
        self.assertEqual(self.ratio.get_raw_score('a', ''), 0)
        self.assertEqual(self.ratio.get_raw_score('', 'a'), 0)
        self.assertEqual(self.ratio.get_raw_score('abc', ''), 0)
        self.assertEqual(self.ratio.get_raw_score('', 'abc'), 0)
        self.assertEqual(self.ratio.get_raw_score('', ''), 0)
        self.assertEqual(self.ratio.get_raw_score('a', 'a'), 100)
        self.assertEqual(self.ratio.get_raw_score('abc', 'abc'), 100)
        
        self.assertEqual(self.ratio.get_raw_score('a', 'ab'), 100)
        self.assertEqual(self.ratio.get_raw_score('b', 'ab'), 100)
        self.assertEqual(self.ratio.get_raw_score(' ac', 'abc'), 67)
        self.assertEqual(self.ratio.get_raw_score('abcdefg', 'xabxcdxxefxgx'), 57)
        self.assertEqual(self.ratio.get_raw_score('ab', 'a'), 100)
        self.assertEqual(self.ratio.get_raw_score('ab', 'A'), 0)
        self.assertEqual(self.ratio.get_raw_score('Ab', 'a'), 0)
        self.assertEqual(self.ratio.get_raw_score('Ab', 'A'), 100)
        self.assertEqual(self.ratio.get_raw_score('Ab', 'b'), 100)
        self.assertEqual(self.ratio.get_raw_score('ab', 'b'), 100)
        self.assertEqual(self.ratio.get_raw_score('abc', 'ac'), 50)
        self.assertEqual(self.ratio.get_raw_score('xabxcdxxefxgx', 'abcdefg'), 57)

        self.assertEqual(self.ratio.get_raw_score('a', 'b'), 0)
        self.assertEqual(self.ratio.get_raw_score('ab', 'ac'), 50)
        self.assertEqual(self.ratio.get_raw_score('ac', 'bc'), 50)
        self.assertEqual(self.ratio.get_raw_score('abc', 'axc'), 67)
        self.assertEqual(self.ratio.get_raw_score('xabxcdxxefxgx', '1ab2cd34ef5g6'), 54)
        self.assertEqual(self.ratio.get_raw_score('example', 'samples'), 71)
        
        self.assertEqual(self.ratio.get_raw_score('bag_distance', 'frankenstein'), 36)
        self.assertEqual(self.ratio.get_raw_score('distance', 'difference'), 38)
        self.assertEqual(self.ratio.get_raw_score('java was neat', 'scala is great'), 62)
        self.assertEqual(self.ratio.get_raw_score('java wAs nEat', 'scala is great'), 54)
        self.assertEqual(self.ratio.get_raw_score('c++ was neat', 'java was neat'), 75)
        
    def test_valid_input_sim_score(self):
        self.assertAlmostEqual(self.ratio.get_sim_score('a', ''), 0.0)
        self.assertAlmostEqual(self.ratio.get_sim_score('', 'a'), 0.0)
        self.assertAlmostEqual(self.ratio.get_sim_score('abc', ''), 0.0)
        self.assertAlmostEqual(self.ratio.get_sim_score('', 'abc'), 0.0)
        self.assertAlmostEqual(self.ratio.get_sim_score('', ''), 0.0)
        self.assertAlmostEqual(self.ratio.get_sim_score('a', 'a'), 1.0)
        self.assertAlmostEqual(self.ratio.get_sim_score('abc', 'abc'), 1.0)
        
        self.assertAlmostEqual(self.ratio.get_sim_score('a', 'ab'), 1.0)
        self.assertAlmostEqual(self.ratio.get_sim_score('b', 'ab'), 1.0)
        self.assertAlmostEqual(self.ratio.get_sim_score(' ac', 'abc'), 0.67)
        self.assertAlmostEqual(self.ratio.get_sim_score('abcdefg', 'xabxcdxxefxgx'), 0.57)
        self.assertAlmostEqual(self.ratio.get_sim_score('ab', 'a'), 1.0)
        self.assertAlmostEqual(self.ratio.get_sim_score('ab', 'A'), 0.0)
        self.assertAlmostEqual(self.ratio.get_sim_score('Ab', 'a'), 0.0)
        self.assertAlmostEqual(self.ratio.get_sim_score('Ab', 'A'), 1.0)
        self.assertAlmostEqual(self.ratio.get_sim_score('Ab', 'b'), 1.0)
        self.assertAlmostEqual(self.ratio.get_sim_score('ab', 'b'), 1.0)
        self.assertAlmostEqual(self.ratio.get_sim_score('abc', 'ac'), 0.50)
        self.assertAlmostEqual(self.ratio.get_sim_score('xabxcdxxefxgx', 'abcdefg'), 0.57)
        
        self.assertAlmostEqual(self.ratio.get_sim_score('a', 'b'), 0.0)
        self.assertAlmostEqual(self.ratio.get_sim_score('ab', 'ac'), 0.50)
        self.assertAlmostEqual(self.ratio.get_sim_score('ac', 'bc'), 0.50)
        self.assertAlmostEqual(self.ratio.get_sim_score('abc', 'axc'), 0.67)
        self.assertAlmostEqual(self.ratio.get_sim_score('xabxcdxxefxgx', '1ab2cd34ef5g6'), 0.54)
        self.assertAlmostEqual(self.ratio.get_sim_score('example', 'samples'), 0.71)
        
        self.assertAlmostEqual(self.ratio.get_sim_score('bag_distance', 'frankenstein'), 0.36)
        self.assertAlmostEqual(self.ratio.get_sim_score('distance', 'difference'), 0.38)
        self.assertAlmostEqual(self.ratio.get_sim_score('java was neat', 'scala is great'), 0.62)
        self.assertAlmostEqual(self.ratio.get_sim_score('java wAs nEat', 'scala is great'), 0.54)
        self.assertAlmostEqual(self.ratio.get_sim_score('c++ was neat', 'java was neat'), 0.75)
    
    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.ratio.get_raw_score('a', None)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.ratio.get_raw_score(None, 'b')

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.ratio.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.ratio.get_raw_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.ratio.get_raw_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.ratio.get_raw_score(12.90, 12.90)

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.ratio.get_sim_score('a', None)

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.ratio.get_sim_score(None, 'b')

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.ratio.get_sim_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_sim_score(self):
        self.ratio.get_sim_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_sim_score(self):
        self.ratio.get_sim_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_sim_score(self):
        self.ratio.get_sim_score(12.90, 12.90)
        
class RatioTestCases(unittest.TestCase):
    def setUp(self):
        self.ratio = Ratio()

    def test_valid_input_raw_score(self):
        self.assertEqual(self.ratio.get_raw_score('a', ''), 0)
        self.assertEqual(self.ratio.get_raw_score('', 'a'), 0)
        self.assertEqual(self.ratio.get_raw_score('abc', ''), 0)
        self.assertEqual(self.ratio.get_raw_score('', 'abc'), 0)
        self.assertEqual(self.ratio.get_raw_score('', ''), 0)
        self.assertEqual(self.ratio.get_raw_score('a', 'a'), 100)
        self.assertEqual(self.ratio.get_raw_score('abc', 'abc'), 100)

        self.assertEqual(self.ratio.get_raw_score('a', 'ab'), 67)
        self.assertEqual(self.ratio.get_raw_score('b', 'ab'), 67)
        self.assertEqual(self.ratio.get_raw_score(' ac', 'abc'), 67)
        self.assertEqual(self.ratio.get_raw_score('abcdefg', 'xabxcdxxefxgx'), 70)
        self.assertEqual(self.ratio.get_raw_score('ab', 'a'), 67)
        self.assertEqual(self.ratio.get_raw_score('ab', 'A'), 0)
        self.assertEqual(self.ratio.get_raw_score('Ab', 'a'), 0)
        self.assertEqual(self.ratio.get_raw_score('Ab', 'A'), 67)
        self.assertEqual(self.ratio.get_raw_score('Ab', 'b'), 67)
        self.assertEqual(self.ratio.get_raw_score('ab', 'b'), 67)
        self.assertEqual(self.ratio.get_raw_score('abc', 'ac'), 80)
        self.assertEqual(self.ratio.get_raw_score('xabxcdxxefxgx', 'abcdefg'), 70)
        self.assertEqual(self.ratio.get_raw_score('a', 'b'), 0)
        self.assertEqual(self.ratio.get_raw_score('ab', 'ac'), 50)
        self.assertEqual(self.ratio.get_raw_score('ac', 'bc'), 50)
        self.assertEqual(self.ratio.get_raw_score('abc', 'axc'), 67)
        self.assertEqual(self.ratio.get_raw_score('xabxcdxxefxgx', '1ab2cd34ef5g6'), 54)
        self.assertEqual(self.ratio.get_raw_score('example', 'samples'), 71)

        self.assertEqual(self.ratio.get_raw_score('bag_distance', 'frankenstein'), 33)
        self.assertEqual(self.ratio.get_raw_score('distance', 'difference'), 56)
        self.assertEqual(self.ratio.get_raw_score('java was neat', 'scala is great'), 59)
        self.assertEqual(self.ratio.get_raw_score('java wAs nEat', 'scala is great'), 52)
        self.assertEqual(self.ratio.get_raw_score('scaLA is greAT', 'java wAs nEat'), 30)

    def test_valid_input_sim_score(self):
        self.assertAlmostEqual(self.ratio.get_sim_score('a', ''), 0.0)
        self.assertAlmostEqual(self.ratio.get_sim_score('', 'a'), 0.0)
        self.assertAlmostEqual(self.ratio.get_sim_score('abc', ''), 0.0)
        self.assertAlmostEqual(self.ratio.get_sim_score('', 'abc'), 0.0)
        self.assertAlmostEqual(self.ratio.get_sim_score('', ''), 0.0)
        self.assertAlmostEqual(self.ratio.get_sim_score('a', 'a'), 1.0)
        self.assertAlmostEqual(self.ratio.get_sim_score('abc', 'abc'), 1.0)

        self.assertAlmostEqual(self.ratio.get_sim_score('a', 'ab'), 0.67)
        self.assertAlmostEqual(self.ratio.get_sim_score('b', 'ab'), 0.67)
        self.assertAlmostEqual(self.ratio.get_sim_score(' ac', 'abc'), 0.67)
        self.assertAlmostEqual(self.ratio.get_sim_score('abcdefg', 'xabxcdxxefxgx'), 0.70)
        self.assertAlmostEqual(self.ratio.get_sim_score('ab', 'a'), 0.67)
        self.assertAlmostEqual(self.ratio.get_sim_score('ab', 'A'), 0.0)
        self.assertAlmostEqual(self.ratio.get_sim_score('Ab', 'a'), 0.0)
        self.assertAlmostEqual(self.ratio.get_sim_score('Ab', 'A'), 0.67)
        self.assertAlmostEqual(self.ratio.get_sim_score('Ab', 'b'), 0.67)
        self.assertAlmostEqual(self.ratio.get_sim_score('ab', 'b'), 0.67)
        self.assertAlmostEqual(self.ratio.get_sim_score('abc', 'ac'), 0.80)
        self.assertAlmostEqual(self.ratio.get_sim_score('xabxcdxxefxgx', 'abcdefg'), 0.70)
        self.assertAlmostEqual(self.ratio.get_sim_score('a', 'b'), 0.0)
        self.assertAlmostEqual(self.ratio.get_sim_score('ab', 'ac'), 0.50)
        self.assertAlmostEqual(self.ratio.get_sim_score('ac', 'bc'), 0.50)
        self.assertAlmostEqual(self.ratio.get_sim_score('abc', 'axc'), 0.67)
        self.assertAlmostEqual(self.ratio.get_sim_score('xabxcdxxefxgx', '1ab2cd34ef5g6'), 0.54)
        self.assertAlmostEqual(self.ratio.get_sim_score('example', 'samples'), 0.71)

        self.assertAlmostEqual(self.ratio.get_sim_score('bag_distance', 'frankenstein'), 0.33)
        self.assertAlmostEqual(self.ratio.get_sim_score('distance', 'difference'), 0.56)
        self.assertAlmostEqual(self.ratio.get_sim_score('java was neat', 'scala is great'), 0.59)
        self.assertAlmostEqual(self.ratio.get_sim_score('java wAs nEat', 'scala is great'), 0.52)
        self.assertAlmostEqual(self.ratio.get_sim_score('scaLA is greAT', 'java wAs nEat'), 0.30)

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.ratio.get_raw_score('a', None)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.ratio.get_raw_score(None, 'b')

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.ratio.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.ratio.get_raw_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.ratio.get_raw_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.ratio.get_raw_score(12.90, 12.90)

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.ratio.get_sim_score('a', None)

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.ratio.get_sim_score(None, 'b')

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.ratio.get_sim_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_sim_score(self):
        self.ratio.get_sim_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_sim_score(self):
        self.ratio.get_sim_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_sim_score(self):
        self.ratio.get_sim_score(12.90, 12.90)


class PartialTokenSortTestCases(unittest.TestCase):
    def setUp(self):
        self.partialTokenSort = PartialTokenSort()

    def test_valid_input_raw_score(self):
        self.assertEqual(self.partialTokenSort.get_raw_score('a', ''), 0)
        self.assertEqual(self.partialTokenSort.get_raw_score('', 'a'), 0)
        self.assertEqual(self.partialTokenSort.get_raw_score('abc', ''), 0)
        self.assertEqual(self.partialTokenSort.get_raw_score('', 'abc'), 0)
        self.assertEqual(self.partialTokenSort.get_raw_score('', ''), 0)
        self.assertEqual(self.partialTokenSort.get_raw_score('a', 'a'), 100)
        self.assertEqual(self.partialTokenSort.get_raw_score('abc', 'abc'), 100)
        self.assertEqual(self.partialTokenSort.get_raw_score('a', 'ab'), 100)
        self.assertEqual(self.partialTokenSort.get_raw_score('b', 'ab'), 100)
        self.assertEqual(self.partialTokenSort.get_raw_score(' ac', 'abc'), 50)
        self.assertEqual(self.partialTokenSort.get_raw_score('abcdefg', 'xabxcdxxefxgx'), 57)
        self.assertEqual(self.partialTokenSort.get_raw_score('ab', 'a'), 100)
        self.assertEqual(self.partialTokenSort.get_raw_score('ab', 'A'), 100)
        self.assertEqual(self.partialTokenSort.get_raw_score('Ab', 'a'), 100)
        self.assertEqual(self.partialTokenSort.get_raw_score('Ab', 'A'), 100)
        self.assertEqual(self.partialTokenSort.get_raw_score('Ab', 'b'), 100)
        self.assertEqual(self.partialTokenSort.get_raw_score('ab', 'b'), 100)
        self.assertEqual(self.partialTokenSort.get_raw_score('abc', 'ac'), 50)
        self.assertEqual(self.partialTokenSort.get_raw_score('xabxcdxxefxgx', 'abcdefg'), 57)
        self.assertEqual(self.partialTokenSort.get_raw_score('a', 'b'), 0)
        self.assertEqual(self.partialTokenSort.get_raw_score('ab', 'ac'), 50)
        self.assertEqual(self.partialTokenSort.get_raw_score('ac', 'bc'), 50)
        self.assertEqual(self.partialTokenSort.get_raw_score('abc', 'axc'), 67)
        self.assertEqual(self.partialTokenSort.get_raw_score('xabxcdxxefxgx', '1ab2cd34ef5g6'), 54)
        self.assertEqual(self.partialTokenSort.get_raw_score('example', 'samples'), 71)
        self.assertEqual(self.partialTokenSort.get_raw_score('bag_distance', 'frankenstein'), 36)
        self.assertEqual(self.partialTokenSort.get_raw_score('distance', 'difference'), 38)
        self.assertEqual(self.partialTokenSort.get_raw_score('java was neat', 'scala is great'), 38)
        self.assertEqual(self.partialTokenSort.get_raw_score('java wAs nEat', 'scala is great'), 38)
        self.assertEqual(self.partialTokenSort.get_raw_score('great is scala', 'java is great'), 77)
        self.assertEqual(self.partialTokenSort.get_raw_score('Wisconsin Badgers vs Chicago Bears', 'Chicago Bears vs Wisconsin Badgers'), 100)
        self.assertEqual(self.partialTokenSort.get_raw_score('Badgers vs Chicago Bears', 'Chicago Bears vs Wisconsin Badgers'), 100)
        self.assertEqual(self.partialTokenSort.get_raw_score('C++ and Java', 'Java and Python'), 80)
        self.assertEqual(self.partialTokenSort.get_raw_score('C++\u00C1 Java\u00C2', 'Java C++'), 100)
        self.assertEqual(self.partialTokenSort.get_raw_score('C++\u00C1 Java\u00C2', 'Java C++', force_ascii=True), 100)
        self.assertEqual(self.partialTokenSort.get_raw_score('C++\u00C1 Java\u00C2', 'Java C++', force_ascii=True), 100)
        self.assertEqual(self.partialTokenSort.get_raw_score('C++\u00C1 Java\u00C2', 'Java C++', full_process=True), 100)
        self.assertEqual(self.partialTokenSort.get_raw_score('C++\u00C1 Java\u00C2', 'Java C++', force_ascii=False), 100)
        self.assertLess(self.partialTokenSort.get_raw_score('C++\u00C1 Java\u00C2', 'Java C++', full_process=False), 100)
        self.assertLess(self.partialTokenSort.get_raw_score('Java C++', 'C++\u00C1 Java\u00C2', full_process=False), 100)
        self.assertLess(self.partialTokenSort.get_raw_score('Java C++', 'C++\u00C1 Java\u00C2', force_ascii=False, full_process=False), 100)
        self.assertLess(self.partialTokenSort.get_raw_score('   Java C++', 'C++\u00C1 Java\u00C2', force_ascii=False, full_process=False), 100)
        self.assertEqual(self.partialTokenSort.get_raw_score('   Java C++', 'C++\u00C1 Java\u00C2', force_ascii=False, full_process=True), 100)
        self.assertLess(self.partialTokenSort.get_raw_score('   Java C++', 'C++\u00C1 Java\u00C2', force_ascii=True, full_process=False), 100)
        self.assertEqual(self.partialTokenSort.get_raw_score('   Java C++', 'C++\u00C1 Java\u00C2', force_ascii=False, full_process=True), 100)

    def test_valid_input_sim_score(self):
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('a', ''), 0.0)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('', 'a'), 0.0)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('abc', ''), 0.0)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('', 'abc'), 0.0)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('', ''), 0.0)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('a', 'a'), 1.0)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('abc', 'abc'), 1.0)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('a', 'ab'), 1.0)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('b', 'ab'), 1.0)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score(' ac', 'abc'), 0.50)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('abcdefg', 'xabxcdxxefxgx'), 0.57)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('ab', 'a'), 1.0)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('ab', 'A'), 1.0)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('Ab', 'a'), 1.0)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('Ab', 'A'), 1.0)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('Ab', 'b'), 1.0)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('ab', 'b'), 1.0)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('abc', 'ac'), 0.50)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('xabxcdxxefxgx', 'abcdefg'), 0.57)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('a', 'b'), 0.0)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('ab', 'ac'), 0.50)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('ac', 'bc'), 0.50)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('abc', 'axc'), 0.67)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('xabxcdxxefxgx', '1ab2cd34ef5g6'), 0.54)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('example', 'samples'), 0.71)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('bag_distance', 'frankenstein'), 0.36)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('distance', 'difference'), 0.38)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('java was neat', 'scala is great'), 0.38)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('java wAs nEat', 'scala is great'), 0.38)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('great is scala', 'java is great'), 0.77)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('Wisconsin Badgers vs Chicago Bears', 'Chicago Bears vs Wisconsin Badgers'), 1.0)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('Badgers vs Chicago Bears', 'Chicago Bears vs Wisconsin Badgers'), 1.0)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('C++ and Java', 'Java and Python'), 0.8)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('C++\u00C1 Java\u00C2', 'Java C++'), 1.0)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('C++\u00C1 Java\u00C2', 'Java C++', force_ascii=True), 1.0)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('C++\u00C1 Java\u00C2', 'Java C++', force_ascii=True), 1.0)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('C++\u00C1 Java\u00C2', 'Java C++', full_process=True), 1.0)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('C++\u00C1 Java\u00C2', 'Java C++', force_ascii=False), 1.0)
        self.assertLess(self.partialTokenSort.get_sim_score('C++\u00C1 Java\u00C2', 'Java C++', full_process=False), 1.0)
        self.assertLess(self.partialTokenSort.get_sim_score('Java C++', 'C++\u00C1 Java\u00C2', full_process=False), 100)
        self.assertLess(self.partialTokenSort.get_sim_score('Java C++', 'C++\u00C1 Java\u00C2', force_ascii=False, full_process=False), 1.0)
        self.assertLess(self.partialTokenSort.get_sim_score('   Java C++', 'C++\u00C1 Java\u00C2', force_ascii=False, full_process=False), 1.0)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('   Java C++', 'C++\u00C1 Java\u00C2', force_ascii=False, full_process=True), 1.0)
        self.assertLess(self.partialTokenSort.get_sim_score('   Java C++', 'C++\u00C1 Java\u00C2', force_ascii=True, full_process=False), 1.0)
        self.assertAlmostEqual(self.partialTokenSort.get_sim_score('   Java C++', 'C++\u00C1 Java\u00C2', force_ascii=False, full_process=True), 1.0)

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.partialTokenSort.get_raw_score('a', None)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.partialTokenSort.get_raw_score(None, 'b')

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.partialTokenSort.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.partialTokenSort.get_raw_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.partialTokenSort.get_raw_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.partialTokenSort.get_raw_score(12.90, 12.90)

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.partialTokenSort.get_sim_score('a', None)

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.partialTokenSort.get_sim_score(None, 'b')

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.partialTokenSort.get_sim_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_sim_score(self):
        self.partialTokenSort.get_sim_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_sim_score(self):
        self.partialTokenSort.get_sim_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_sim_score(self):
        self.partialTokenSort.get_sim_score(12.90, 12.90)

class TokenSortTestCases(unittest.TestCase):
    def setUp(self):
        self.tokenSort = TokenSort()

    def test_valid_input_raw_score(self):
        self.assertEqual(self.tokenSort.get_raw_score('a', ''), 0)
        self.assertEqual(self.tokenSort.get_raw_score('', 'a'), 0)
        self.assertEqual(self.tokenSort.get_raw_score('abc', ''), 0)
        self.assertEqual(self.tokenSort.get_raw_score('', 'abc'), 0)
        self.assertEqual(self.tokenSort.get_raw_score('', ''), 0)
        self.assertEqual(self.tokenSort.get_raw_score('a', 'a'), 100)
        self.assertEqual(self.tokenSort.get_raw_score('abc', 'abc'), 100)
        self.assertEqual(self.tokenSort.get_raw_score('a', 'ab'), 67)
        self.assertEqual(self.tokenSort.get_raw_score('b', 'ab'), 67)
        self.assertEqual(self.tokenSort.get_raw_score(' ac', 'abc'), 80)
        self.assertEqual(self.tokenSort.get_raw_score('abcdefg', 'xabxcdxxefxgx'), 70)
        self.assertEqual(self.tokenSort.get_raw_score('ab', 'a'), 67)
        self.assertEqual(self.tokenSort.get_raw_score('ab', 'A'), 67)
        self.assertEqual(self.tokenSort.get_raw_score('Ab', 'a'), 67)
        self.assertEqual(self.tokenSort.get_raw_score('Ab', 'A'), 67)
        self.assertEqual(self.tokenSort.get_raw_score('Ab', 'b'), 67)
        self.assertEqual(self.tokenSort.get_raw_score('ab', 'b'), 67)
        self.assertEqual(self.tokenSort.get_raw_score('abc', 'ac'), 80)
        self.assertEqual(self.tokenSort.get_raw_score('xabxcdxxefxgx', 'abcdefg'), 70)
        self.assertEqual(self.tokenSort.get_raw_score('a', 'b'), 0)
        self.assertEqual(self.tokenSort.get_raw_score('ab', 'ac'), 50)
        self.assertEqual(self.tokenSort.get_raw_score('ac', 'bc'), 50)
        self.assertEqual(self.tokenSort.get_raw_score('abc', 'axc'), 67)
        self.assertEqual(self.tokenSort.get_raw_score('xabxcdxxefxgx', '1ab2cd34ef5g6'), 54)
        self.assertEqual(self.tokenSort.get_raw_score('example', 'samples'), 71)
        self.assertEqual(self.tokenSort.get_raw_score('bag_distance', 'frankenstein'), 33)
        self.assertEqual(self.tokenSort.get_raw_score('distance', 'difference'), 56)
        self.assertEqual(self.tokenSort.get_raw_score('java was neat', 'scala is great'), 37)
        self.assertEqual(self.tokenSort.get_raw_score('java wAs nEat', 'scala is great'), 37)
        self.assertEqual(self.tokenSort.get_raw_score('great is scala', 'java is great'), 81)
        self.assertEqual(self.tokenSort.get_raw_score('Wisconsin Badgers vs Chicago Bears', 'Chicago Bears vs Wisconsin Badgers'), 100)
        self.assertEqual(self.tokenSort.get_raw_score('Badgers vs Chicago Bears', 'Chicago Bears vs Wisconsin Badgers'), 83)
        self.assertEqual(self.tokenSort.get_raw_score('C++ and Java', 'Java and Python'), 64)
        self.assertEqual(self.tokenSort.get_raw_score('C++\u00C1 Java\u00C2', 'Java C++'), 100)
        self.assertEqual(self.tokenSort.get_raw_score('C++\u00C1 Java\u00C2', 'Java C++', force_ascii=True), 100)
        self.assertEqual(self.tokenSort.get_raw_score('C++\u00C1 Java\u00C2', 'Java C++', force_ascii=True), 100)
        self.assertEqual(self.tokenSort.get_raw_score('C++\u00C1 Java\u00C2', 'Java C++', full_process=True), 100)
        self.assertLess(self.tokenSort.get_raw_score('C++\u00C1 Java\u00C2', 'Java C++', force_ascii=False), 100)
        self.assertLess(self.tokenSort.get_raw_score('C++\u00C1 Java\u00C2', 'Java C++', full_process=False), 100)
        self.assertLess(self.tokenSort.get_raw_score('Java C++', 'C++\u00C1 Java\u00C2', full_process=False), 100)
        self.assertLess(self.tokenSort.get_raw_score('Java C++', 'C++\u00C1 Java\u00C2', force_ascii=False, full_process=False), 100)
        self.assertLess(self.tokenSort.get_raw_score('   Java C++', 'C++\u00C1 Java\u00C2', force_ascii=False, full_process=False), 100)
        self.assertLess(self.tokenSort.get_raw_score('   Java C++', 'C++\u00C1 Java\u00C2', force_ascii=False, full_process=True), 100)
        self.assertLess(self.tokenSort.get_raw_score('   Java C++', 'C++\u00C1 Java\u00C2', force_ascii=True, full_process=False), 100)
        self.assertLess(self.tokenSort.get_raw_score('   Java C++', 'C++\u00C1 Java\u00C2', force_ascii=False, full_process=True), 100)

    def test_valid_input_sim_score(self):
        self.assertAlmostEqual(self.tokenSort.get_sim_score('a', ''), 0.0)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('', 'a'), 0.0)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('abc', ''), 0.0)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('', 'abc'), 0.0)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('', ''), 0.0)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('a', 'a'), 1.0)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('abc', 'abc'), 1.0)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('a', 'ab'), 0.67)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('b', 'ab'), 0.67)
        self.assertAlmostEqual(self.tokenSort.get_sim_score(' ac', 'abc'), 0.80)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('abcdefg', 'xabxcdxxefxgx'), 0.70)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('ab', 'a'), 0.67)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('ab', 'A'), 0.67)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('Ab', 'a'), 0.67)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('Ab', 'A'), 0.67)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('Ab', 'b'), 0.67)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('ab', 'b'), 0.67)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('abc', 'ac'), 0.80)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('xabxcdxxefxgx', 'abcdefg'), 0.70)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('a', 'b'), 0.0)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('ab', 'ac'), 0.50)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('ac', 'bc'), 0.50)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('abc', 'axc'), 0.67)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('xabxcdxxefxgx', '1ab2cd34ef5g6'), 0.54)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('example', 'samples'), 0.71)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('bag_distance', 'frankenstein'), 0.33)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('distance', 'difference'), 0.56)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('java was neat', 'scala is great'), 0.37)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('java wAs nEat', 'scala is great'), 0.37)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('great is scala', 'java is great'), 0.81)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('Wisconsin Badgers vs Chicago Bears', 'Chicago Bears vs Wisconsin Badgers'), 1.0)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('Badgers vs Chicago Bears', 'Chicago Bears vs Wisconsin Badgers'), 0.83)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('C++ and Java', 'Java and Python'), 0.64)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('C++\u00C1 Java\u00C2', 'Java C++'), 1.0)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('C++\u00C1 Java\u00C2', 'Java C++', force_ascii=True), 1.0)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('C++\u00C1 Java\u00C2', 'Java C++', force_ascii=True), 1.0)
        self.assertAlmostEqual(self.tokenSort.get_sim_score('C++\u00C1 Java\u00C2', 'Java C++', full_process=True), 1.0)
        self.assertLess(self.tokenSort.get_sim_score('C++\u00C1 Java\u00C2', 'Java C++', force_ascii=False), 1.0)
        self.assertLess(self.tokenSort.get_sim_score('C++\u00C1 Java\u00C2', 'Java C++', full_process=False), 1.0)
        self.assertLess(self.tokenSort.get_sim_score('Java C++', 'C++\u00C1 Java\u00C2', full_process=False), 100)
        self.assertLess(self.tokenSort.get_sim_score('Java C++', 'C++\u00C1 Java\u00C2', force_ascii=False, full_process=False), 1.0)
        self.assertLess(self.tokenSort.get_sim_score('   Java C++', 'C++\u00C1 Java\u00C2', force_ascii=False, full_process=False), 1.0)
        self.assertLess(self.tokenSort.get_sim_score('   Java C++', 'C++\u00C1 Java\u00C2', force_ascii=False, full_process=True), 1.0)
        self.assertLess(self.tokenSort.get_sim_score('   Java C++', 'C++\u00C1 Java\u00C2', force_ascii=True, full_process=False), 1.0)
        self.assertLess(self.tokenSort.get_sim_score('   Java C++', 'C++\u00C1 Java\u00C2', force_ascii=False, full_process=True), 1.0)

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.tokenSort.get_raw_score('a', None)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.tokenSort.get_raw_score(None, 'b')

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.tokenSort.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.tokenSort.get_raw_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.tokenSort.get_raw_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.tokenSort.get_raw_score(12.90, 12.90)

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.tokenSort.get_sim_score('a', None)

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.tokenSort.get_sim_score(None, 'b')

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.tokenSort.get_sim_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_sim_score(self):
        self.tokenSort.get_sim_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_sim_score(self):
        self.tokenSort.get_sim_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_sim_score(self):
        self.tokenSort.get_sim_score(12.90, 12.90)
