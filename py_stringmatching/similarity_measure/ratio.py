"""Fuzzy Wuzzy Ratio Similarity Measure"""

from __future__ import division

from difflib import SequenceMatcher
from py_stringmatching import utils
from py_stringmatching.similarity_measure.sequence_similarity_measure import \
                                                    SequenceSimilarityMeasure


class Ratio(SequenceSimilarityMeasure):
    """Computes Fuzzy Wuzzy ratio similarity measure.

    Fuzzy Wuzzy ratio raw score is a measure of the strings similarity as an int in the
    range [0, 100]. For two strings X and Y, the score is defined by 
    int(round((2.0 * M / T) * 100)) where T is the total number of characters in 
    both strings, and M is the number of matches in the two strings. Fuzzy Wuzzy ratio
    sim score is a float in the range [0, 1] and is obtained by dividing the raw score
    by 100.
        
     Note:
         In the case where either of strings X or Y are empty, we define the
         Fuzzy Wuzzy ratio similarity score to be 0. 
    """
    def __init__(self):
        pass

    def get_raw_score(self, string1, string2):
        """
        Computes the Fuzzy Wuzzy ratio measure raw score between two strings.
        This score is in the range [0,100].

        Args:
            string1,string2 (str): Input strings

        Returns:
            Ratio measure raw score (int) is returned

        Raises:
            TypeError: If the inputs are not strings

        Examples:
            >>> s = Ratio()
            >>> s.get_raw_score('Robert', 'Rupert')
            67
            >>> s.get_raw_score('Sue', 'sue')
            67
            >>> s.get_raw_score('example', 'samples')
            71

        References:
            * https://pypi.python.org/pypi/fuzzywuzzy
        """
        # input validations
        utils.sim_check_for_none(string1, string2)
        utils.sim_check_for_string_inputs(string1, string2)

        # if one of the strings is empty return 0
        if utils.sim_check_for_empty(string1, string2):
            return 0

        string1 = utils.convert_to_unicode(string1)
        string2 = utils.convert_to_unicode(string2)

        sm = SequenceMatcher(None, string1, string2)
        return int(round(100 * sm.ratio()))

    def get_sim_score(self, string1, string2):
        """
        Computes the Fuzzy Wuzzy ratio similarity score between two strings.
        This score is in the range [0,1].

        Args:
            string1,string2 (str): Input strings

        Returns:
            Ratio measure similarity score (float) is returned

        Raises:
            TypeError: If the inputs are not strings

        Examples:
            >>> s = Ratio()
            >>> s.get_sim_score('Robert', 'Rupert')
            0.67
            >>> s.get_sim_score('Sue', 'sue')
            0.67
            >>> s.get_sim_score('example', 'samples')
            0.71

        References:
            * https://pypi.python.org/pypi/fuzzywuzzy
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
