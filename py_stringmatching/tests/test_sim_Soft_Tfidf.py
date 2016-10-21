# coding=utf-8

from __future__ import unicode_literals

import math
import unittest

from nose.tools import *

from py_stringmatching.similarity_measure.jaro_winkler import JaroWinkler
from py_stringmatching.similarity_measure.affine import Affine
from py_stringmatching.similarity_measure.soft_tfidf import SoftTfIdf
from py_stringmatching.similarity_measure.jaro import Jaro

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