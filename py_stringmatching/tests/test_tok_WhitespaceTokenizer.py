from __future__ import unicode_literals

import unittest
from nose.tools import *

from py_stringmatching.tokenizer.whitespace_tokenizer import WhitespaceTokenizer

class WhitespaceTokenizerTestCases(unittest.TestCase):
    def setUp(self):
        self.ws_tok = WhitespaceTokenizer()
        self.ws_tok_return_set = WhitespaceTokenizer(return_set=True)

    def test_whitespace_tok_valid(self):
        self.assertEqual(self.ws_tok.tokenize('data science'),
                         ['data', 'science'])
        self.assertEqual(self.ws_tok.tokenize('data        science'),
                         ['data', 'science'])
        self.assertEqual(self.ws_tok.tokenize('data   science'),
                         ['data', 'science'])
        self.assertEqual(self.ws_tok.tokenize('data\tscience'),
                         ['data', 'science'])
        self.assertEqual(self.ws_tok.tokenize('data\nscience'),
                         ['data', 'science'])
        self.assertEqual(self.ws_tok.tokenize('ab cd ab bb cd db'),
                         ['ab', 'cd', 'ab', 'bb', 'cd', 'db'])
        self.assertEqual(self.ws_tok_return_set.tokenize('ab cd ab bb cd db'),
                         ['ab', 'cd', 'bb', 'db'])

    def test_get_return_set(self):
        self.assertEqual(self.ws_tok.get_return_set(), False)
        self.assertEqual(self.ws_tok_return_set.get_return_set(), True)

    def test_set_return_set(self):
        tok = WhitespaceTokenizer()
        self.assertEqual(tok.get_return_set(), False)
        self.assertEqual(tok.tokenize('ab cd ab bb cd db'),
                         ['ab', 'cd', 'ab', 'bb', 'cd', 'db'])
        self.assertEqual(tok.set_return_set(True), True)
        self.assertEqual(tok.get_return_set(), True)
        self.assertEqual(tok.tokenize('ab cd ab bb cd db'),
                         ['ab', 'cd', 'bb', 'db'])
        self.assertEqual(tok.set_return_set(False), True)
        self.assertEqual(tok.get_return_set(), False)
        self.assertEqual(tok.tokenize('ab cd ab bb cd db'),
                         ['ab', 'cd', 'ab', 'bb', 'cd', 'db'])

    def test_get_delim_set(self):
        self.assertSetEqual(self.ws_tok.get_delim_set(), {' ', '\t', '\n'})

    @raises(TypeError)
    def test_whitespace_tok_invalid1(self):
        self.ws_tok.tokenize(None)

    @raises(TypeError)
    def test_whitespace_tok_invalid2(self):
        self.ws_tok.tokenize(99)

    @raises(AttributeError)
    def test_set_delim_set(self):
        self.ws_tok.set_delim_set({'*', '.'})