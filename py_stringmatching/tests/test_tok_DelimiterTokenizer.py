from __future__ import unicode_literals

import unittest
from nose.tools import *

from py_stringmatching.tokenizer.delimiter_tokenizer import DelimiterTokenizer

class DelimiterTokenizerTestCases(unittest.TestCase):
    def setUp(self):
        self.delim_tok1 = DelimiterTokenizer()
        self.delim_tok2 = DelimiterTokenizer(set([',']))
        self.delim_tok3 = DelimiterTokenizer(set(['*', '.']))
        self.delim_tok4 = DelimiterTokenizer(set(['..', 'ab']))    
        self.delim_tok4_list = DelimiterTokenizer(['..', 'ab', '..'])
        self.delim_tok4_return_set = DelimiterTokenizer(set(['..', 'ab']),
                                                        return_set=True)

    def test_delimiter_valid(self):
        self.assertEqual(self.delim_tok1.tokenize('data science'),
                         ['data', 'science'])
        self.assertEqual(self.delim_tok2.tokenize('data,science'),
                         ['data', 'science'])
        self.assertEqual(self.delim_tok2.tokenize('data science'),
                         ['data science'])
        self.assertEqual(self.delim_tok3.tokenize('ab cd*ef.*bb. gg.'),
                         ['ab cd', 'ef', 'bb', ' gg'])
        self.assertEqual(
            self.delim_tok4.tokenize('ab cd..efabbb....ggab cd..efabgh'),
            [' cd', 'ef', 'bb', 'gg', ' cd', 'ef', 'gh'])
        self.assertEqual(
            self.delim_tok4_list.tokenize('ab cd..efabbb....ggab cd..efabgh'),
            [' cd', 'ef', 'bb', 'gg', ' cd', 'ef', 'gh'])
        self.assertEqual(
            self.delim_tok4_return_set.tokenize(
                'ab cd..efabbb....ggab cd..efabgh'),
            [' cd', 'ef', 'bb', 'gg', 'gh'])

    def test_get_return_set(self):
        self.assertEqual(self.delim_tok4.get_return_set(), False)
        self.assertEqual(self.delim_tok4_return_set.get_return_set(), True)

    def test_get_delim_set(self):
        self.assertSetEqual(self.delim_tok1.get_delim_set(), {' '})
        self.assertSetEqual(self.delim_tok3.get_delim_set(), {'*', '.'})
        self.assertSetEqual(self.delim_tok4_list.get_delim_set(), {'..', 'ab'})

    def test_set_return_set(self):
        tok = DelimiterTokenizer(set(['..', 'ab']))
        self.assertEqual(tok.get_return_set(), False)
        self.assertEqual(
            tok.tokenize('ab cd..efabbb....ggab cd..efabgh'),
            [' cd', 'ef', 'bb', 'gg', ' cd', 'ef', 'gh'])
        self.assertEqual(tok.set_return_set(True), True)
        self.assertEqual(tok.get_return_set(), True)
        self.assertEqual(
            tok.tokenize('ab cd..efabbb....ggab cd..efabgh'),
            [' cd', 'ef', 'bb', 'gg', 'gh'])
        self.assertEqual(tok.set_return_set(False), True)
        self.assertEqual(tok.get_return_set(), False)
        self.assertEqual(
            tok.tokenize('ab cd..efabbb....ggab cd..efabgh'),
            [' cd', 'ef', 'bb', 'gg', ' cd', 'ef', 'gh'])

    def test_set_delim_set(self):
        tok = DelimiterTokenizer(['*', '.'])
        self.assertSetEqual(tok.get_delim_set(), {'*', '.'})
        self.assertEqual(tok.tokenize('ab cd*ef.*bb. gg.'),
                         ['ab cd', 'ef', 'bb', ' gg'])      
        self.assertEqual(tok.set_delim_set({'..', 'ab'}), True)
        self.assertSetEqual(tok.get_delim_set(), {'..', 'ab'})
        self.assertEqual(
            tok.tokenize('ab cd..efabbb....ggab cd..efabgh'),
            [' cd', 'ef', 'bb', 'gg', ' cd', 'ef', 'gh'])

    @raises(TypeError)
    def test_delimiter_invalid1(self):
        invalid_delim_tok = DelimiterTokenizer(set([',', 10]))

    @raises(TypeError)
    def test_delimiter_invalid2(self):
        self.delim_tok1.tokenize(None)

    @raises(TypeError)
    def test_delimiter_invalid3(self):
        self.delim_tok1.tokenize(99)