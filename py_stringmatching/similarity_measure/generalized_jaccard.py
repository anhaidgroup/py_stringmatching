"""Generalized jaccard similarity measure"""

from py_stringmatching import utils
from py_stringmatching.similarity_measure.jaro import Jaro
from py_stringmatching.similarity_measure.hybrid_similarity_measure import \
                                                    HybridSimilarityMeasure


class GeneralizedJaccard(HybridSimilarityMeasure):
    """Generalized jaccard similarity measure class.

    Parameters:
        sim_func (function): similarity function. This should return a similarity score between two strings in set (optional),
                             default is jaro similarity measure
        threshold (float): Threshold value (defaults to 0.5). If the similarity of a token pair exceeds the threshold,
                           then the token pair is considered a match.
    """
    def __init__(self, sim_func=Jaro().get_raw_score, threshold=0.5):
        self.sim_func = sim_func
        self.threshold = threshold
        super(GeneralizedJaccard, self).__init__()

    def get_raw_score(self, set1, set2):
        """
        Computes the Generalized Jaccard measure between two sets.

        This similarity measure is softened version of the Jaccard measure. The Jaccard measure is
        promising candidate for tokens which exactly match across the sets. However, in practice tokens
        are often misspelled, such as energy vs. eneryg. THe generalized Jaccard measure will enable
        matching in such cases.

        Args:
            set1,set2 (set or list): Input sets (or lists) of strings. Input lists are converted to sets.

        Returns:
            Generalized Jaccard similarity (float)

        Raises:
            TypeError : If the inputs are not sets (or lists) or if one of the inputs is None.
            ValueError : If the similarity measure doesn't return values in the range [0,1]

        Examples:
            >>> gj = GeneralizedJaccard()
            >>> gj.get_raw_score(['data', 'science'], ['data'])
            0.5
            >>> gj.get_raw_score(['data', 'management'], ['data', 'data', 'science'])
            0.3333333333333333
            >>> gj.get_raw_score(['Niall'], ['Neal', 'Njall'])
            0.43333333333333335
            >>> gj = GeneralizedJaccard(sim_func=JaroWinkler().get_raw_score, threshold=0.8)
            >>> gj.get_raw_score(['Comp', 'Sci.', 'and', 'Engr', 'Dept.,', 'Universty', 'of', 'Cal,', 'San', 'Deigo'],
                                 ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego'])
            0.45810185185185187
        """
        # input validations
        utils.sim_check_for_none(set1, set2)
        utils.sim_check_for_list_or_set_inputs(set1, set2)

        # if exact match return 1.0
        if utils.sim_check_for_exact_match(set1, set2):
            return 1.0

        # if one of the strings is empty return 0
        if utils.sim_check_for_empty(set1, set2):
            return 0

        if not isinstance(set1, set):
            set1 = set(set1)
        if not isinstance(set2, set):
            set2 = set(set2)

        set1_x = set()
        set2_y = set()
        match_score = 0.0
        match_count = 0
        list_matches = []
        for element in set1:
            for item in set2:
                score = self.sim_func(element, item)
                if score > 1 or score < 0:
                    raise ValueError('Similarity measure should' + \
                                     ' return value in the range [0,1]')
                if score > self.threshold:
                    list_matches.append((element, item, score))

        # position of first string, second string and sim score in tuple
        first_string_pos = 0
        second_string_pos = 1
        sim_score_pos = 2

        # sort the score of all the pairs
        list_matches.sort(key=lambda x: x[sim_score_pos], reverse=True)

        # select score in increasing order of their weightage, 
        # do not reselect the same element from either set.
        for element in list_matches:
            if (element[first_string_pos] not in set1_x and
                element[second_string_pos] not in set2_y):
                set1_x.add(element[first_string_pos])
                set2_y.add(element[second_string_pos])
                match_score += element[sim_score_pos]
                match_count += 1

        return round(float(match_score) / float(len(set1) + len(set2) - match_count),5)

    def get_sim_score(self, set1, set2):
        """
        Computes the normalized Generalized Jaccard similarity between two sets.

        Args:
            set1,set2 (set or list): Input sets (or lists) of strings. Input lists are converted to sets.

        Returns:
            Normalized Generalized Jaccard similarity (float)

        Raises:
            TypeError : If the inputs are not sets (or lists) or if one of the inputs is None.
            ValueError : If the similarity measure doesn't return values in the range [0,1]

        Examples:
            >>> gj = GeneralizedJaccard()
            >>> gj.get_sim_score(['data', 'science'], ['data'])
            0.5
            >>> gj.get_sim_score(['data', 'management'], ['data', 'data', 'science'])
            0.3333333333333333
            >>> gj.get_sim_score(['Niall'], ['Neal', 'Njall'])
            0.43333333333333335
            >>> gj = GeneralizedJaccard(sim_func=JaroWinkler().get_raw_score, threshold=0.8)
            >>> gj.get_sim_score(['Comp', 'Sci.', 'and', 'Engr', 'Dept.,', 'Universty', 'of', 'Cal,', 'San', 'Deigo'],
                                 ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego'])
            0.45810185185185187

        """
        return self.get_raw_score(set1, set2)

    def get_sim_func(self):
        """
        Get similarity function

        Returns:
            similarity function (function)
        """
        return self.sim_func

    def get_threshold(self):
        """
        Get threshold used for the similarity function

        Returns:
            threshold (float)
        """
        return self.threshold

    def set_sim_func(self, sim_func):
        """
        Set similarity function

        Args:
            sim_func (function): similarity function
        """
        self.sim_func = sim_func
        return True

    def set_threshold(self, threshold):
        """
        Set threshold value for the similarity function

        Args:
            threshold (float): threshold value
        """
        self.threshold = threshold
        return True
