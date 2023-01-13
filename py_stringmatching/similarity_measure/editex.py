# coding=utf-8
"""Editex distance measure"""

from __future__ import division
from __future__ import unicode_literals
import unicodedata
import six

import numpy as np

from py_stringmatching import utils
from six.moves import xrange
from six import text_type
from py_stringmatching.similarity_measure.sequence_similarity_measure import \
                                                    SequenceSimilarityMeasure


class Editex(SequenceSimilarityMeasure):
    """Editex distance measure class.

    Parameters:
        match_cost (int): Weight to give the correct char match, default=0
        group_cost (int): Weight to give if the chars are in the same editex group, default=1
        mismatch_cost (int): Weight to give the incorrect char match, default=2
        local (boolean): Local variant on/off, default=False
    """
    def __init__(self, match_cost=0, group_cost=1, mismatch_cost=2,
                 local=False):
        self.match_cost = match_cost
        self.group_cost = group_cost
        self.mismatch_cost = mismatch_cost
        self.local = local
        super(Editex, self).__init__()

    def get_raw_score(self, string1, string2):
        """
        Computes the editex distance between two strings.

        As described on pages 3 & 4 of
        Zobel, Justin and Philip Dart. 1996. Phonetic string matching: Lessons from
        information retrieval. In: Proceedings of the ACM-SIGIR Conference on
        Research and Development in Information Retrieval, Zurich, Switzerland.
        166–173. http://goanna.cs.rmit.edu.au/~jz/fulltext/sigir96.pdf

        The local variant is based on
        Ring, Nicholas and Alexandra L. Uitdenbogerd. 2009. Finding ‘Lucy in
        Disguise’: The Misheard Lyric Matching Problem. In: Proceedings of the 5th
        Asia Information Retrieval Symposium, Sapporo, Japan. 157-167.
        http://www.seg.rmit.edu.au/research/download.php?manuscript=404

        Args:
            string1,string2 (str): Input strings

        Returns:
            Editex distance (int)

        Raises:
            TypeError : If the inputs are not strings

        Examples:
            >>> ed = Editex()
            >>> ed.get_raw_score('cat', 'hat')
            2
            >>> ed.get_raw_score('Niall', 'Neil')
            2
            >>> ed.get_raw_score('aluminum', 'Catalan')
            12
            >>> ed.get_raw_score('ATCG', 'TAGC')
            6

        References:
            * Abydos Library - https://github.com/chrislit/abydos/blob/master/abydos/distance.py

        """
        # input validations
        utils.sim_check_for_none(string1, string2)
        utils.sim_check_for_string_inputs(string1, string2)
        if utils.sim_check_for_exact_match(string1, string2):
            return 0

        # convert both the strings to NFKD normalized unicode
        string1 = unicodedata.normalize('NFKD', text_type(string1.upper()))
        string2 = unicodedata.normalize('NFKD', text_type(string2.upper()))

        # convert ß to SS (for Python2)
        string1 = string1.replace('ß', 'SS')
        string2 = string2.replace('ß', 'SS')

        if len(string1) == 0:
            return len(string2) * self.mismatch_cost
        if len(string2) == 0:
            return len(string1) * self.mismatch_cost

        d_mat = np.zeros((len(string1) + 1, len(string2) + 1), dtype=int)
        len1 = len(string1)
        len2 = len(string2)
        string1 = ' ' + string1
        string2 = ' ' + string2
        editex_helper = EditexHelper(self.match_cost, self.mismatch_cost,
                                     self.group_cost)

        if not self.local:
            for i in xrange(1, len1 + 1):
                d_mat[i, 0] = d_mat[i - 1, 0] + editex_helper.d_cost(
                                                    string1[i - 1], string1[i])

        for j in xrange(1, len2 + 1):
            d_mat[0, j] = d_mat[0, j - 1] + editex_helper.d_cost(string2[j - 1],
                                                                 string2[j])

        for i in xrange(1, len1 + 1):
            for j in xrange(1, len2 + 1):
                d_mat[i, j] = min(d_mat[i - 1, j] + editex_helper.d_cost(
                                                    string1[i - 1], string1[i]),
                                  d_mat[i, j - 1] + editex_helper.d_cost(
                                                    string2[j - 1], string2[j]),
                                  d_mat[i - 1, j - 1] + editex_helper.r_cost(
                                                        string1[i], string2[j]))

        return d_mat[len1, len2]

    def get_sim_score(self, string1, string2):
        """
        Computes the normalized editex similarity between two strings.

        Args:
            string1,string2 (str): Input strings

        Returns:
            Normalized editex similarity (float)

        Raises:
            TypeError : If the inputs are not strings

        Examples:
            >>> ed = Editex()
            >>> ed.get_sim_score('cat', 'hat')
            0.66666666666666674
            >>> ed.get_sim_score('Niall', 'Neil')
            0.80000000000000004
            >>> ed.get_sim_score('aluminum', 'Catalan')
            0.25
            >>> ed.get_sim_score('ATCG', 'TAGC')
            0.25

        References:
            * Abydos Library - https://github.com/chrislit/abydos/blob/master/abydos/distance.py
        """
        raw_score = self.get_raw_score(string1, string2)
        string1_len = len(string1)
        string2_len = len(string2)
        if string1_len == 0 and string2_len == 0:
            return 1.0
        return 1 - (raw_score / max(string1_len * self.mismatch_cost,
                                    string2_len * self.mismatch_cost))

    def get_match_cost(self):
        """
        Get match cost

        Returns:
            match cost (int)
        """
        return self.match_cost

    def get_group_cost(self):
        """
        Get group cost

        Returns:
            group cost (int)
        """
        return self.group_cost

    def get_mismatch_cost(self):
        """
        Get mismatch cost

        Returns:
            mismatch cost (int)
        """
        return self.mismatch_cost

    def get_local(self):
        """
        Get local flag

        Returns:
            local flag (boolean)
        """
        return self.local

    def set_match_cost(self, match_cost):
        """
        Set match cost

        Args:
            match_cost (int): Weight to give the correct char match
        """
        self.match_cost = match_cost
        return True

    def set_group_cost(self, group_cost):
        """
        Set group cost

        Args:
            group_cost (int): Weight to give if the chars are in the same editex group
        """
        self.group_cost = group_cost
        return True

    def set_mismatch_cost(self, mismatch_cost):
        """
        Set mismatch cost

        Args:
            mismatch_cost (int): Weight to give the incorrect char match
        """
        self.mismatch_cost = mismatch_cost
        return True

    def set_local(self, local):
        """
        Set local flag

        Args:
            local (boolean): Local variant on/off
        """
        self.local = local
        return True


class EditexHelper:
    letter_groups = dict()
    letter_groups['A'] = letter_groups['E'] = letter_groups['I'] = letter_groups['O'] \
        = letter_groups['U'] = letter_groups['Y'] = 0
    letter_groups['B'] = letter_groups['P'] = 1
    letter_groups['C'] = letter_groups['K'] = letter_groups['Q'] = 2
    letter_groups['D'] = letter_groups['T'] = 3
    letter_groups['L'] = letter_groups['R'] = 4
    letter_groups['M'] = letter_groups['N'] = 5
    letter_groups['G'] = letter_groups['J'] = 6
    letter_groups['F'] = letter_groups['P'] = letter_groups['V'] = 7
    letter_groups['S'] = letter_groups['X'] = letter_groups['Z'] = 8
    letter_groups['C'] = letter_groups['S'] = letter_groups['J'] = 9
    all_letters = frozenset('AEIOUYBPCKQDTLRMNGJFVSXZ')

    def __init__(self, match_cost, mismatch_cost, group_cost):
        self.match_cost = match_cost
        self.mismatch_cost = mismatch_cost
        self.group_cost = group_cost

    def r_cost(self, ch1, ch2):
        """Return r(a,b) according to Zobel & Dart's definition
        """
        if ch1 == ch2:
            return self.match_cost
        if ch1 in EditexHelper.all_letters and ch2 in EditexHelper.all_letters:
            if (EditexHelper.letter_groups[ch1] ==
                EditexHelper.letter_groups[ch2]):
                return self.group_cost
        return self.mismatch_cost

    def d_cost(self, ch1, ch2):
        """Return d(a,b) according to Zobel & Dart's definition
        """
        if ch1 != ch2 and (ch1 == 'H' or ch1 == 'W'):
            return self.group_cost
        return self.r_cost(ch1, ch2)
