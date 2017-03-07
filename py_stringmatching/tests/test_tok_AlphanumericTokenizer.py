from __future__ import unicode_literals

import unittest
from nose.tools import *

from py_stringmatching.tokenizer.alphanumeric_tokenizer import AlphanumericTokenizer

class AlphanumericTokenizerTestCases(unittest.TestCase):
    def setUp(self):
        self.alnum_tok = AlphanumericTokenizer()
        self.alnum_tok_return_set = AlphanumericTokenizer(return_set=True)

    def test_alphanumeric_tok_valid(self):
        self.assertEqual(self.alnum_tok.tokenize(''), [])
        self.assertEqual(self.alnum_tok.tokenize('#$'), [])
        self.assertEqual(self.alnum_tok.tokenize('hello99'), ['hello99'])
        self.assertEqual(
            self.alnum_tok.tokenize(',data9,(science), data9#.(integration).88!'),
            ['data9', 'science', 'data9', 'integration', '88'])
        self.assertEqual(self.alnum_tok_return_set.tokenize(
                             ',data9,(science), data9#.(integration).88!'),
                         ['data9', 'science', 'integration', '88'])

    def test_get_return_set(self):
        self.assertEqual(self.alnum_tok.get_return_set(), False)
        self.assertEqual(self.alnum_tok_return_set.get_return_set(), True)

    def test_set_return_set(self):
        tok = AlphanumericTokenizer()
        self.assertEqual(tok.get_return_set(), False)
        self.assertEqual(
            tok.tokenize(',data9,(science), data9#.(integration).88!'),
            ['data9', 'science', 'data9', 'integration', '88'])
        self.assertEqual(tok.set_return_set(True), True)
        self.assertEqual(tok.get_return_set(), True)
        self.assertEqual(
            tok.tokenize(',data9,(science), data9#.(integration).88!'),
            ['data9', 'science', 'integration', '88'])
        self.assertEqual(tok.set_return_set(False), True)
        self.assertEqual(tok.get_return_set(), False)
        self.assertEqual(
            tok.tokenize(',data9,(science), data9#.(integration).88!'),
            ['data9', 'science', 'data9', 'integration', '88'])

    @raises(TypeError)
    def test_alphanumeric_tok_invalid1(self):
        self.alnum_tok.tokenize(None)

    @raises(TypeError)
    def test_alphanumeric_tok_invalid2(self):
        self.alnum_tok.tokenize(99)