"""Fuzzy Wuzzy Ratio Similarity Measure"""

from __future__ import division

from difflib import SequenceMatcher
from py_stringmatching import utils
from py_stringmatching.similarity_measure.sequence_similarity_measure import \
                                                    SequenceSimilarityMeasure


class Ratio(SequenceSimilarityMeasure):
    """Fuzzy Wuzzy ratio similarity measure class index."""
    def __init__(self):
        pass

    def get_raw_score(self, string1, string2):
        """
        Computes the Fuzzy Wuzzy ratio similarity between two strings.

        Return a measure of the strings similarity as an int in the
        range [0, 100]. Returns int(round((2.0 * M / T) * 100)) where T 
        is the total number of elements in both sequences, and M is the 
        number of matches. 

        Args:
            string1,string2 (str): Input strings

        Returns:
            Ratio similarity score (int) is returned

        Raises:
            TypeError : If the inputs are not strings

        Examples:
            >>> s = Ratio()
            >>> s.get_raw_score('Robert', 'Rupert')
            67
            >>> s.get_raw_score('Sue', 'sue')
            67
            >>> s.get_raw_score('example', 'samples')
            71
        """
        # input validations
        utils.sim_check_for_none(string1, string2)
        utils.sim_check_for_string_inputs(string1, string2)

        # if one of the strings is empty return 0
        if utils.sim_check_for_empty(string1, string2):
            return 0

        sm = SequenceMatcher(None, string1, string2)
        return int(round(100 * sm.ratio()))

    def get_sim_score(self, string1, string2):
        """
        Computes the Fuzzy Wuzzy ratio similarity between two strings.

        Return a measure of the strings similarity as a float in the
        range [0, 100]. Returns ((2.0 * M) / T) where T 
        is the total number of elements in both sequences, and M is the 
        number of matches.  

        Args:
            string1,string2 (str): Input strings

        Returns:
            Ratio similarity score (float) is returned

        Raises:
            TypeError : If the inputs are not strings

        Examples:
            >>> s = Ratio()
            >>> s.get_sim_score('Robert', 'Rupert')
            0.67
            >>> s.get_sim_score('Sue', 'sue')
            0.67
            >>> s.get_sim_score('example', 'samples')
            0.71
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
