# coding=utf-8
"""QWERTY typo distance measure"""

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


class QWERTYex(SequenceSimilarityMeasure):
    """QWERTY typo distance measure class.

    Parameters:
        match_cost (int): Weight to give the correct char match, default=0
        group_cost (int): Weight to give if the chars are in the same QWERTY group, default=1
        mismatch_cost (int): Weight to give the incorrect char match, default=2
        local (boolean): Local variant on/off, default=False
    """
    def __init__(self, match_cost=0, group_cost=1, mismatch_cost=2,
                 local=False):
        self.match_cost = match_cost
        self.group_cost = group_cost
        self.mismatch_cost = mismatch_cost
        self.local = local
        super(QWERTYex, self).__init__()

    def get_raw_score(self, string1, string2):
        """
        Computes the QWERTY typo distance between two strings.

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
            QWERTY typo distance (int)

        Raises:
            TypeError : If the inputs are not strings

        Examples:
            >>> qd = QWERTYex()
            >>> qd.get_raw_score('cat', 'hat')
            2
            >>> qd.get_raw_score('Niall', 'Neil')
            2
            >>> qd.get_raw_score('aluminum', 'Catalan')
            9
            >>> qd.get_raw_score('ATCG', 'TAGC')
            3

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

        d_mat = np.zeros((len(string1) + 1, len(string2) + 1), dtype=np.int)
        len1 = len(string1)
        len2 = len(string2)
        string1 = ' ' + string1
        string2 = ' ' + string2
        qwertyex_helper = QWERTYexHelper(self.match_cost, self.mismatch_cost,
                                     self.group_cost)

        if not self.local:
            for i in xrange(1, len1 + 1):
                d_mat[i, 0] = d_mat[i - 1, 0] + qwertyex_helper.d_cost(
                                                    string1[i - 1], string1[i])

        for j in xrange(1, len2 + 1):
            d_mat[0, j] = d_mat[0, j - 1] + qwertyex_helper.d_cost(string2[j - 1],
                                                                 string2[j])

        for i in xrange(1, len1 + 1):
            for j in xrange(1, len2 + 1):
                d_mat[i, j] = min(d_mat[i - 1, j] + qwertyex_helper.d_cost(
                                                    string1[i - 1], string1[i]),
                                  d_mat[i, j - 1] + qwertyex_helper.d_cost(
                                                    string2[j - 1], string2[j]),
                                  d_mat[i - 1, j - 1] + qwertyex_helper.r_cost(
                                                        string1[i], string2[j]))

        return d_mat[len1, len2]

    def get_sim_score(self, string1, string2):
        """
        Computes the normalized QWERTY typo similarity between two strings.

        Args:
            string1,string2 (str): Input strings

        Returns:
            Normalized QWERTY typo similarity (float)

        Raises:
            TypeError : If the inputs are not strings

        Examples:
            >>> qd = QWERTYex()
            >>> qd.get_sim_score('cat', 'hat')
            0.6666666666666667
            >>> qd.get_sim_score('Niall', 'Neil')
            0.8
            >>> qd.get_sim_score('aluminum', 'Catalan')
            0.4375
            >>> qd.get_sim_score('ATCG', 'TAGC')
            0.625

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
            group_cost (int): Weight to give if the chars are in the same QWERTY group
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


class QWERTYexHelper:
    # QWERTY groups described on page 4 of
    # Ahmad, Indrayana, Wibisono and Ijtihadie. 2017.
    # Edit Distance Weighting Modification using Phonetic and Typographic Letter 
    # Grouping over Homomorphic Encrypted Data. 
    # In: International Conference on Science in Information Technology. 408-412.
    # https://ieeexplore.ieee.org/abstract/document/8257147
    
    letter_groups = {
        'QA', 'QW', 'AQ', 'AW', 'WQ', 'WA', # 1
        'WS', 'WE', 'SW', 'SE', 'EW', 'ES', # 2
        'ED', 'ER', 'DE', 'DR', 'RE', 'RD', # 3
        'RF', 'RT', 'FR', 'FT', 'TR', 'TF', # 4
        'TG', 'TY', 'GT', 'GY', 'YT', 'YG', # 5
        'YH', 'YU', 'HY', 'HU', 'UY', 'UH', # 6
        'UJ', 'UI', 'JU', 'JI', 'IU', 'IJ', # 7
        'IK', 'IO', 'KI', 'KO', 'OI', 'OK', # 8
        'OL', 'OP', 'LO', 'LP', 'PO', 'PL', # 8
        'AZ', 'AS', 'ZA', 'ZS', 'SA', 'SZ', # 10
        'SX', 'SD', 'DS', 'DX', 'XS', 'XD', # 11
        'DC', 'ER', 'DE', 'DR', 'RE', 'RD', # 12
        'FV', 'FG', 'VF', 'VG', 'GF', 'GV', # 13
        'GB', 'GH', 'BG', 'BH', 'HG', 'HB', # 14
        'HN', 'HJ', 'NH', 'NJ', 'JH', 'JN', # 15
        'JM', 'JK', 'MJ', 'MK', 'KJ', 'JN', # 16
        'KL', 'LK', # 17
        'ZX', 'XZ', # 18
        'XC', 'CX', # 19
        'CV', 'VC', # 20
        'VB', 'BV', # 21
        'BN', 'NB', # 22
        'NM', 'MN', # 23 
    }

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
        if ch1 in QWERTYexHelper.all_letters and ch2 in QWERTYexHelper.all_letters:
            if ch1 + ch2 in QWERTYexHelper.letter_groups:
                return self.group_cost
        return self.mismatch_cost

    def d_cost(self, ch1, ch2):
        """Return d(a,b) according to Zobel & Dart's definition
        """
        if ch1 != ch2:
            return self.group_cost
        return self.r_cost(ch1, ch2)
