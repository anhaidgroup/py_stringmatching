from __future__ import unicode_literals

import unittest
from nose.tools import *

from py_stringmatching.tokenizer.alphabetic_tokenizer import AlphabeticTokenizer

class AlphabeticTokenizerTestCases(unittest.TestCase):
    def setUp(self):
        self.al_tok = AlphabeticTokenizer()
        self.al_tok_return_set = AlphabeticTokenizer(return_set=True)

    def test_alphabetic_tok_valid(self):
        self.assertEqual(self.al_tok.tokenize(''), [])
        self.assertEqual(self.al_tok.tokenize('99'), [])
        self.assertEqual(self.al_tok.tokenize('hello'), ['hello'])
        self.assertEqual(self.al_tok.tokenize('ab bc. cd##de ef09 bc fg ab.'),
                         ['ab', 'bc', 'cd', 'de', 'ef', 'bc', 'fg', 'ab'])
        self.assertEqual(
            self.al_tok_return_set.tokenize('ab bc. cd##de ef09 bc fg ab.'),
            ['ab', 'bc', 'cd', 'de', 'ef', 'fg'])

    def test_get_return_set(self):
        self.assertEqual(self.al_tok.get_return_set(), False)
        self.assertEqual(self.al_tok_return_set.get_return_set(), True)

    def test_set_return_set(self):
        tok = AlphabeticTokenizer()
        self.assertEqual(tok.get_return_set(), False)
        self.assertEqual(tok.tokenize('ab bc. cd##de ef09 bc fg ab.'),
                         ['ab', 'bc', 'cd', 'de', 'ef', 'bc', 'fg', 'ab'])
        self.assertEqual(tok.set_return_set(True), True)
        self.assertEqual(tok.get_return_set(), True)
        self.assertEqual(
            tok.tokenize('ab bc. cd##de ef09 bc fg ab.'),
            ['ab', 'bc', 'cd', 'de', 'ef', 'fg'])
        self.assertEqual(tok.set_return_set(False), True)
        self.assertEqual(tok.get_return_set(), False)
        self.assertEqual(tok.tokenize('ab bc. cd##de ef09 bc fg ab.'),
                         ['ab', 'bc', 'cd', 'de', 'ef', 'bc', 'fg', 'ab'])

    @raises(TypeError)
    def test_alphabetic_tok_invalid1(self):
        self.al_tok.tokenize(None)

    @raises(TypeError)
    def test_alphabetic_tok_invalid2(self):
        self.al_tok.tokenize(99)