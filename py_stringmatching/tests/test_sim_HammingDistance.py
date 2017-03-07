# coding=utf-8

from __future__ import unicode_literals

import math
import unittest

from nose.tools import *

from py_stringmatching.similarity_measure.hamming_distance import HammingDistance

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