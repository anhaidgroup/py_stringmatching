"""Fuzzy Wuzzy Partial Ratio Similarity Measure"""

from __future__ import division

from difflib import SequenceMatcher
from py_stringmatching import utils
from py_stringmatching.similarity_measure.sequence_similarity_measure import \
                                                    SequenceSimilarityMeasure


class PartialRatio(SequenceSimilarityMeasure):
    """Fuzzy Wuzzy partial ratio similarity measure class index."""
    def __init__(self):
        pass

    def get_raw_score(self, string1, string2):
        """
        Computes the Fuzzy Wuzzy partial ratio similarity between two strings.

        Return a measure of the strings similarity as a int in the
        range [0, 100]. Given two strings, let the shorter string be of length m.
        It finds the ratio similarity measure between the shorter string and every
        substring of length m of the longer string, and returns the maximum of
        those similarity measures.

        Args:
            string1,string2 (str): Input strings

        Returns:
            Partial Ratio similarity score (int) is returned

        Raises:
            TypeError : If the inputs are not strings

        Examples:
            >>> s = PartialRatio()
            >>> s.get_raw_score('Robert Rupert', 'Rupert')
            100
            >>> s.get_raw_score('Sue', 'sue')
            67
            >>> s.get_raw_score('example', 'samples')
            86
        """
        # input validations
        utils.sim_check_for_none(string1, string2)
        utils.sim_check_for_string_inputs(string1, string2)

        # if one of the strings is empty return 0
        if utils.sim_check_for_empty(string1, string2):
            return 0

        # string1 should be smaller in length than string2. If this is not the case
        # then swap string1 and string2
        if len(string1) > len(string2):
            temp = string1
            string1 = string2
            string2 = temp

        sm = SequenceMatcher(None, string1, string2)
        matching_blocks = sm.get_matching_blocks()

        scores = []
        for block in matching_blocks:
            string2_starting_index = 0
            if (block[1] - block[0] > 0):
                string2_starting_index = block[1] - block[0]
            string2_ending_index = string2_starting_index + len(string1)
            string2_substr = string2[string2_starting_index:string2_ending_index]

            sm2 = SequenceMatcher(None, string1, string2_substr)
            similarity_ratio = sm2.ratio()
            if similarity_ratio > .995:
                return 100
            else:
                scores.append(similarity_ratio)

        return int(round(100 * max(scores)))

    def get_sim_score(self, string1, string2):
        """
        Computes the Fuzzy Wuzzy partial ratio similarity between two strings.

        Return a measure of the strings similarity as a float in the
        range [0, 1]. Given two strings, let the shorter string be of length m.
        It finds the ratio similarity measure between the shorter string and every
        substring of length m of the longer string, and returns the maximum of
        those similarity measures.

        Args:
            string1,string2 (str): Input strings

        Returns:
            Partial Ratio similarity score (float) is returned

        Raises:
            TypeError : If the inputs are not strings

        Examples:
            >>> s = PartialRatio()
            >>> s.get_raw_score('Robert Rupert', 'Rupert')
            1.0
            >>> s.get_raw_score('Sue', 'sue')
            0.67
            >>> s.get_raw_score('example', 'samples')
            0.86
        """
        # input validations
        utils.sim_check_for_none(string1, string2)
        utils.sim_check_for_string_inputs(string1, string2)

        # if one of the strings is empty return 0
        if utils.sim_check_for_empty(string1, string2):
            return 0

        raw_score = 1.0 * self.get_raw_score(string1, string2)
        sim_score = raw_score / 100
        return sim_score
