# coding=utf-8

from __future__ import unicode_literals

import math
import unittest

from nose.tools import *

from py_stringmatching.similarity_measure.soundex import Soundex

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