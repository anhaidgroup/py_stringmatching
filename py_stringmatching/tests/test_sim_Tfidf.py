# coding=utf-8

from __future__ import unicode_literals

import math
import unittest

from nose.tools import *

from py_stringmatching.similarity_measure.tfidf import TfIdf

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