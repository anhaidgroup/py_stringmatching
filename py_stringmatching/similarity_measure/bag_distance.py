"""Bag distance measure"""

import collections

from py_stringmatching import utils
from py_stringmatching.similarity_measure.sequence_similarity_measure import \
                                                    SequenceSimilarityMeasure


class BagDistance(SequenceSimilarityMeasure):
    """Bag distance measure class.
    """
    def __init__(self):
        super(BagDistance, self).__init__()

    def get_raw_score(self, string1, string2):
        """
        Computes the bag distance between two strings.

        For two strings X and Y, the Bag distance is:
        :math:`max( |bag(string1)-bag(string2)|, |bag(string2)-bag(string1)| )`

        Args:
            string1,string2 (str): Input strings

        Returns:
            Bag distance (int)

        Raises:
            TypeError : If the inputs are not strings

        Examples:
            >>> bd = BagDistance()
            >>> bd.get_raw_score('cat', 'hat')
            1
            >>> bd.get_raw_score('Niall', 'Neil')
            2
            >>> bd.get_raw_score('aluminum', 'Catalan')
            5
            >>> bd.get_raw_score('ATCG', 'TAGC')
            0
            >>> bd.get_raw_score('abcde', 'xyz')
            5

        References:
            * String Matching with Metric Trees Using an Approximate Distance: http://www-db.disi.unibo.it/research/papers/SPIRE02.pdf
        """
        # input validations
        utils.sim_check_for_none(string1, string2)
        utils.sim_check_for_string_inputs(string1, string2)
        if utils.sim_check_for_exact_match(string1, string2):
            return 0

        len_str1 = len(string1)
        len_str2 = len(string2)

        if len_str1 == 0:
            return len_str2

        if len_str2 == 0:
            return len_str1

        bag1 = collections.Counter(string1)
        bag2 = collections.Counter(string2)

        size1 = sum((bag1 - bag2).values())
        size2 = sum((bag2 - bag1).values())

        # returning the max of difference of sets
        return max(size1, size2)

    def get_sim_score(self, string1, string2):
        """
        Computes the normalized bag similarity between two strings.

        Args:
            string1,string2 (str): Input strings

        Returns:
            Normalized bag similarity (float)

        Raises:
            TypeError : If the inputs are not strings

        Examples:
            >>> bd = BagDistance()
            >>> bd.get_sim_score('cat', 'hat')
            0.6666666666666667
            >>> bd.get_sim_score('Niall', 'Neil')
            0.6
            >>> bd.get_sim_score('aluminum', 'Catalan')
            0.375
            >>> bd.get_sim_score('ATCG', 'TAGC')
            1.0
            >>> bd.get_sim_score('abcde', 'xyz')
            0.0

        References:
            * String Matching with Metric Trees Using an Approximate Distance: http://www-db.disi.unibo.it/research/papers/SPIRE02.pdf
        """
        raw_score = self.get_raw_score(string1, string2)
        string1_len = len(string1)
        string2_len = len(string2)
        if string1_len == 0 and string2_len == 0:
            return 1.0
        return 1 - (raw_score / max(string1_len, string2_len))
