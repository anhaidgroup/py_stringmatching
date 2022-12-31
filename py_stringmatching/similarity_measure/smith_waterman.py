# coding=utf-8

from py_stringmatching.similarity_measure.cython.cython_utils import cython_sim_ident
from py_stringmatching import utils
from py_stringmatching.similarity_measure.sequence_similarity_measure import \
                                                    SequenceSimilarityMeasure
from py_stringmatching.similarity_measure.cython.cython_smith_waterman import smith_waterman


class SmithWaterman(SequenceSimilarityMeasure):
    """Computes Smith-Waterman measure.

    The Smith-Waterman algorithm performs local sequence alignment; that is, for determining similar regions
    between two strings. Instead of looking at the total sequence, the Smith–Waterman algorithm compares segments of
    all possible lengths and optimizes the similarity measure. See the string matching chapter in the DI book (Principles of Data Integration). 

    Args:
        gap_cost (float): Cost of gap (defaults to 1.0).
        sim_func (function): Similarity function to give a score for the correspondence between the characters (defaults
                             to an identity function, which returns 1 if the two characters are the same and 0 otherwise).

    Attributes:
        gap_cost (float): An attribute to store the gap cost.
        sim_func (function): An attribute to store the similarity function.
    """

    def __init__(self, gap_cost=1.0, sim_func=cython_sim_ident):
        self.gap_cost = gap_cost
        self.sim_func = sim_func
        super(SmithWaterman, self).__init__()

    def get_raw_score(self, string1, string2):
        """Computes the raw Smith-Waterman score between two strings.

        Args:
            string1,string2 (str) : Input strings.

        Returns:
            Smith-Waterman similarity score (float).

        Raises:
            TypeError : If the inputs are not strings or if one of the inputs is None.

        Examples:
            >>> sw = SmithWaterman()
            >>> sw.get_raw_score('cat', 'hat')
            2.0
            >>> sw = SmithWaterman(gap_cost=2.2)
            >>> sw.get_raw_score('dva', 'deeve')
            1.0
            >>> sw = SmithWaterman(gap_cost=1, sim_func=lambda s1, s2 : (2 if s1 == s2 else -1))
            >>> sw.get_raw_score('dva', 'deeve')
            2.0
            >>> sw = SmithWaterman(gap_cost=1.4, sim_func=lambda s1, s2 : (1.5 if s1 == s2 else 0.5))
            >>> sw.get_raw_score('GCATAGCU', 'GATTACA')
            6.5
        """
        
        # input validations
        utils.sim_check_for_none(string1, string2)

        # convert input to unicode.
        string1 = utils.convert_to_unicode(string1)
        string2 = utils.convert_to_unicode(string2)

        utils.tok_check_for_string_input(string1, string2)

        # Returns smith waterman similarity score from cython function
        return smith_waterman(string1,string2,self.gap_cost,self.sim_func)

    def get_gap_cost(self):
        """Get gap cost.

        Returns:
            Gap cost (float).
        """
        return self.gap_cost

    def get_sim_func(self):
        """Get similarity function.

        Returns:
            Similarity function (function).
        """
        return self.sim_func

    def set_gap_cost(self, gap_cost):
        """Set gap cost.

        Args:
            gap_cost (float): Cost of gap.
        """
        self.gap_cost = gap_cost
        return True

    def set_sim_func(self, sim_func):
        """Set similarity function.

        Args:
            sim_func (function): Similarity function to give a score for the correspondence between the characters.
        """
        self.sim_func = sim_func
        return True
