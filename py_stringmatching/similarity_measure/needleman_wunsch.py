from py_stringmatching import utils
from py_stringmatching.similarity_measure.sequence_similarity_measure import \
                                                    SequenceSimilarityMeasure
from py_stringmatching.similarity_measure.cython.cython_needleman_wunsch import needleman_wunsch
from py_stringmatching.similarity_measure.cython.cython_utils import cython_sim_ident


class NeedlemanWunsch(SequenceSimilarityMeasure):
    """Computes Needleman-Wunsch measure.

    The Needleman-Wunsch distance generalizes the Levenshtein distance and considers global alignment between two strings.
    Specifically, it is computed by assigning a score to each alignment between the two input strings and choosing the
    score of the best alignment, that is, the maximal score. An alignment between two strings is a set of correspondences
    between their characters, allowing for gaps.

    Args:
        gap_cost (float): Cost of gap (defaults to 1.0).
        sim_func (function): Similarity function to give a score for each correspondence between the characters (defaults
                             to an identity function, which returns 1 if the two characters are the same and 0 otherwise.  
                             
    Attributes:
        gap_cost (float): An attribute to store the gap cost.
        sim_func (function): An attribute to store the similarity function.
    """

    def __init__(self, gap_cost=1.0, sim_func=cython_sim_ident):
        self.gap_cost = gap_cost
        self.sim_func = sim_func
        super(NeedlemanWunsch, self).__init__()

    def get_raw_score(self, string1, string2):
        """Computes the raw Needleman-Wunsch score between two strings.

        Args:
            string1,string2 (str) : Input strings.

        Returns:
            Needleman-Wunsch similarity score (float).

        Raises:
            TypeError : If the inputs are not strings or if one of the inputs is None.

        Examples:
            >>> nw = NeedlemanWunsch()
            >>> nw.get_raw_score('dva', 'deeva')
            1.0
            >>> nw = NeedlemanWunsch(gap_cost=0.0)
            >>> nw.get_raw_score('dva', 'deeve')
            2.0
            >>> nw = NeedlemanWunsch(gap_cost=1.0, sim_func=lambda s1, s2 : (2.0 if s1 == s2 else -1.0))
            >>> nw.get_raw_score('dva', 'deeve')
            1.0
            >>> nw = NeedlemanWunsch(gap_cost=0.5, sim_func=lambda s1, s2 : (1.0 if s1 == s2 else -1.0))
            >>> nw.get_raw_score('GCATGCUA', 'GATTACA')
            2.5
        """
        
        # input validations
        utils.sim_check_for_none(string1, string2)

        # convert input to unicode.
        string1 = utils.convert_to_unicode(string1)
        string2 = utils.convert_to_unicode(string2)

        utils.tok_check_for_string_input(string1, string2)

        # returns the similarity score from the cython function
        return needleman_wunsch(string1, string2, self.gap_cost, self.sim_func)

    def get_gap_cost(self):
        """Get gap cost.

        Returns:
            Gap cost (float).
        """
        return self.gap_cost

    def get_sim_func(self):
        """Get the similarity function.

        Returns:
            similarity function (function).
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
            sim_func (function): Similarity function to give a score for the correspondence between characters.
        """
        self.sim_func = sim_func
        return True
