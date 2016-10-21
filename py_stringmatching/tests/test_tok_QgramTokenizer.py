from __future__ import unicode_literals

import unittest
from nose.tools import *

from py_stringmatching.tokenizer.qgram_tokenizer import QgramTokenizer

class QgramTokenizerTestCases(unittest.TestCase):
    def setUp(self):
        self.qg1_tok = QgramTokenizer(qval=1, padding=False)
        self.qg2_tok = QgramTokenizer(padding=False)
        self.qg2_tok_return_set = QgramTokenizer(padding=False,return_set=True)
        self.qg3_tok = QgramTokenizer(qval=3, padding=False)
        self.qg1_tok_wipad = QgramTokenizer(qval=1)
        self.qg2_tok_wipad = QgramTokenizer()
        self.qg2_tok_wipad_return_set = QgramTokenizer(return_set=True)
        self.qg3_tok_wipad = QgramTokenizer(qval=3)
        self.qg3_tok_wipad_diffpad = QgramTokenizer(qval=3,prefix_pad='^',
                                                    suffix_pad='!')

    def test_qgrams_valid(self):
        self.assertEqual(self.qg2_tok.tokenize(''), [])
        self.assertEqual(self.qg2_tok.tokenize('a'), [])
        self.assertEqual(self.qg2_tok.tokenize('aa'), ['aa'])
        self.assertEqual(self.qg2_tok.tokenize('database'),
                         ['da', 'at', 'ta', 'ab', 'ba', 'as', 'se'])
        self.assertEqual(self.qg2_tok.tokenize('aabaabcdba'),
                         ['aa', 'ab', 'ba', 'aa', 'ab', 'bc', 'cd', 'db', 'ba'])
        self.assertEqual(self.qg2_tok_return_set.tokenize('aabaabcdba'),
                         ['aa', 'ab', 'ba', 'bc', 'cd', 'db'])
        self.assertEqual(self.qg1_tok.tokenize('d'), ['d'])
        self.assertEqual(self.qg3_tok.tokenize('database'),
                         ['dat', 'ata', 'tab', 'aba', 'bas', 'ase'])

        self.assertEqual(self.qg2_tok_wipad.tokenize(''), ['#$'])
        self.assertEqual(self.qg2_tok_wipad.tokenize('a'), ['#a', 'a$'])
        self.assertEqual(self.qg2_tok_wipad.tokenize('aa'), ['#a', 'aa', 'a$'])
        self.assertEqual(self.qg2_tok_wipad.tokenize('database'),
                         ['#d', 'da', 'at', 'ta', 'ab', 'ba', 'as', 'se', 'e$'])
        self.assertEqual(self.qg2_tok_wipad.tokenize('aabaabcdba'),
                         ['#a', 'aa', 'ab', 'ba', 'aa', 'ab', 'bc', 'cd', 'db', 'ba', 'a$'])
        self.assertEqual(self.qg2_tok_wipad_return_set.tokenize('aabaabcdba'),
                         ['#a', 'aa', 'ab', 'ba', 'bc', 'cd', 'db', 'a$'])
        self.assertEqual(self.qg1_tok_wipad.tokenize('d'), ['d'])
        self.assertEqual(self.qg3_tok_wipad.tokenize('database'),
                         ['##d', '#da', 'dat', 'ata', 'tab', 'aba', 'bas', 'ase', 'se$', 'e$$'])

        self.assertEqual(self.qg3_tok_wipad_diffpad.tokenize('database'),
                         ['^^d', '^da', 'dat', 'ata', 'tab', 'aba', 'bas',
                          'ase', 'se!', 'e!!'])

    def test_get_return_set(self):
        self.assertEqual(self.qg2_tok.get_return_set(), False)
        self.assertEqual(self.qg2_tok_return_set.get_return_set(), True)
        self.assertEqual(self.qg2_tok_wipad.get_return_set(), False)
        self.assertEqual(self.qg2_tok_wipad_return_set.get_return_set(), True)


    def test_get_qval(self):
        self.assertEqual(self.qg2_tok.get_qval(), 2)
        self.assertEqual(self.qg3_tok.get_qval(), 3)
        self.assertEqual(self.qg2_tok_wipad.get_qval(), 2)
        self.assertEqual(self.qg3_tok_wipad.get_qval(), 3)


    def test_set_return_set(self):
        tok = QgramTokenizer(padding=False)
        self.assertEqual(tok.get_return_set(), False)
        self.assertEqual(tok.tokenize('aabaabcdba'),
                         ['aa', 'ab', 'ba', 'aa', 'ab', 'bc', 'cd', 'db', 'ba'])
        self.assertEqual(tok.set_return_set(True), True)
        self.assertEqual(tok.get_return_set(), True)
        self.assertEqual(tok.tokenize('aabaabcdba'),
                         ['aa', 'ab', 'ba', 'bc', 'cd', 'db'])
        self.assertEqual(tok.set_return_set(False), True)
        self.assertEqual(tok.get_return_set(), False)
        self.assertEqual(tok.tokenize('aabaabcdba'),
                         ['aa', 'ab', 'ba', 'aa', 'ab', 'bc', 'cd', 'db', 'ba'])
        tok = QgramTokenizer()
        self.assertEqual(tok.get_return_set(), False)
        self.assertEqual(tok.tokenize('aabaabcdba'),
                         ['#a', 'aa', 'ab', 'ba', 'aa', 'ab', 'bc', 'cd', 'db', 'ba', 'a$'])
        self.assertEqual(tok.set_return_set(True), True)
        self.assertEqual(tok.get_return_set(), True)
        self.assertEqual(tok.tokenize('aabaabcdba'),
                         ['#a', 'aa', 'ab', 'ba', 'bc', 'cd', 'db', 'a$'])
        self.assertEqual(tok.set_return_set(False), True)
        self.assertEqual(tok.get_return_set(), False)
        self.assertEqual(tok.tokenize('aabaabcdba'),
                         ['#a', 'aa', 'ab', 'ba', 'aa', 'ab', 'bc', 'cd', 'db', 'ba', 'a$'])



    def test_set_qval(self):
        tok = QgramTokenizer(padding=False)
        self.assertEqual(tok.get_qval(), 2)
        self.assertEqual(tok.tokenize('database'),
                         ['da', 'at', 'ta', 'ab', 'ba', 'as', 'se'])
        self.assertEqual(tok.set_qval(3), True)
        self.assertEqual(tok.get_qval(), 3)
        self.assertEqual(tok.tokenize('database'),
                         ['dat', 'ata', 'tab', 'aba', 'bas', 'ase'])

        tok = QgramTokenizer()
        self.assertEqual(tok.get_qval(), 2)
        self.assertEqual(tok.tokenize('database'),
                         ['#d', 'da', 'at', 'ta', 'ab', 'ba', 'as', 'se', 'e$'])
        self.assertEqual(tok.set_qval(3), True)
        self.assertEqual(tok.get_qval(), 3)
        self.assertEqual(tok.tokenize('database'),
                         ['##d', '#da', 'dat', 'ata', 'tab', 'aba', 'bas', 'ase', 'se$', 'e$$'])

    def test_set_padding(self):
        tok = QgramTokenizer()
        self.assertEqual(tok.get_padding(), True)
        self.assertEqual(tok.tokenize('database'),
                         ['#d', 'da', 'at', 'ta', 'ab', 'ba', 'as', 'se', 'e$'])
        tok.set_padding(False)
        self.assertEqual(tok.get_padding(), False)
        self.assertEqual(tok.tokenize('database'),
                         ['da', 'at', 'ta', 'ab', 'ba', 'as', 'se'])

    def test_set_prefix_pad(self):
        tok = QgramTokenizer()
        self.assertEqual(tok.get_prefix_pad(), '#')
        self.assertEqual(tok.tokenize('database'),
                         ['#d', 'da', 'at', 'ta', 'ab', 'ba', 'as', 'se', 'e$'])
        tok.set_prefix_pad('^')
        self.assertEqual(tok.get_prefix_pad(), '^')
        self.assertEqual(tok.tokenize('database'),
                         ['^d', 'da', 'at', 'ta', 'ab', 'ba', 'as', 'se', 'e$'])

    def test_set_suffix_pad(self):
        tok = QgramTokenizer()
        self.assertEqual(tok.get_suffix_pad(), '$')
        self.assertEqual(tok.tokenize('database'),
                         ['#d', 'da', 'at', 'ta', 'ab', 'ba', 'as', 'se', 'e$'])
        tok.set_suffix_pad('!')
        self.assertEqual(tok.get_suffix_pad(), '!')
        self.assertEqual(tok.tokenize('database'),
                         ['#d', 'da', 'at', 'ta', 'ab', 'ba', 'as', 'se', 'e!'])

    @raises(TypeError)
    def test_qgrams_none(self):
        self.qg2_tok.tokenize(None)

    @raises(AssertionError)
    def test_qgrams_invalid1(self):
        invalid_qg_tok = QgramTokenizer(0) 

    @raises(TypeError)
    def test_qgrams_invalid2(self):
        self.qg2_tok.tokenize(99)

    @raises(AssertionError)
    def test_set_qval_invalid(self):
        qg_tok = QgramTokenizer()
        qg_tok.set_qval(0)

    @raises(AssertionError)
    def test_padding_invalid(self):
        _ = QgramTokenizer(padding=10)

    @raises(AssertionError)
    def test_set_padding_invalid(self):
        qg = QgramTokenizer()
        qg.set_padding(10)

    @raises(AssertionError)
    def test_prefixpad_invalid1(self):
        _ = QgramTokenizer(prefix_pad=10)

    @raises(AssertionError)
    def test_prefixpad_invalid2(self):
        _ = QgramTokenizer(prefix_pad="###")

    @raises(AssertionError)
    def test_set_prefix_pad_invalid1(self):
        qg = QgramTokenizer()
        qg.set_prefix_pad(10)

    @raises(AssertionError)
    def test_set_prefix_pad_invalid2(self):
        qg = QgramTokenizer()
        qg.set_prefix_pad('###')

    @raises(AssertionError)
    def test_suffixpad_invalid1(self):
        _ = QgramTokenizer(suffix_pad=10)

    @raises(AssertionError)
    def test_suffixpad_invalid2(self):
        _ = QgramTokenizer(suffix_pad="###")

    @raises(AssertionError)
    def test_set_suffix_pad_invalid1(self):
        qg = QgramTokenizer()
        qg.set_suffix_pad(10)

    @raises(AssertionError)
    def test_set_suffix_pad_invalid2(self):
        qg = QgramTokenizer()
        qg.set_suffix_pad('###')