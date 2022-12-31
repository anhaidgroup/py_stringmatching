
from py_stringmatching import utils
from py_stringmatching.similarity_measure.sequence_similarity_measure import \
                                                    SequenceSimilarityMeasure
from py_stringmatching.similarity_measure.cython.cython_affine import affine
from py_stringmatching.similarity_measure.cython.cython_utils import cython_sim_ident

class Affine(SequenceSimilarityMeasure):
    """Returns the affine gap score between two strings. 

    The affine gap measure is an extension of the Needleman-Wunsch measure that handles the longer gaps more
    gracefully. For more information refer to the string matching chapter in the DI book ("Principles of Data Integration").

    Args:
        gap_start (float): Cost for the gap at the start (defaults to 1).
        gap_continuation (float): Cost for the gap continuation (defaults to 0.5).
        sim_func (function): Function computing similarity score between two characters, which are represented as strings (defaults
                             to an identity function, which returns 1 if the two characters are the same and returns 0 otherwise). 

    Attributes:
        gap_start (float): An attribute to store the gap cost at the start.
        gap_continuation (float): An attribute to store the gap continuation cost.
        sim_func (function): An attribute to store the similarity function.
    """

    def __init__(self, gap_start=1, gap_continuation=0.5, sim_func=cython_sim_ident):
        self.gap_start = gap_start
        self.gap_continuation = gap_continuation
        self.sim_func = sim_func
        super(Affine, self).__init__()

    def get_raw_score(self, string1, string2):
        """Computes the affine gap score between two strings. This score can be outside the range [0,1].
        
        Args:
            string1,string2 (str) : Input strings.

        Returns:
            Affine gap score betwen the two input strings (float).

        Raises:
            TypeError : If the inputs are not strings or if one of the inputs is None.

        Examples:
            >>> aff = Affine()
            >>> aff.get_raw_score('dva', 'deeva')
            1.5
            >>> aff = Affine(gap_start=2, gap_continuation=0.5)
            >>> aff.get_raw_score('dva', 'deeve')
            -0.5
            >>> aff = Affine(gap_continuation=0.2, sim_func=lambda s1, s2: (int(1 if s1 == s2 else 0)))
            >>> aff.get_raw_score('AAAGAATTCA', 'AAATCA')
            4.4
        """
        # input validations
        utils.sim_check_for_none(string1, string2)

        # convert input to unicode.
        string1 = utils.convert_to_unicode(string1)
        string2 = utils.convert_to_unicode(string2)

        utils.tok_check_for_string_input(string1, string2)

        # if one of the strings is empty return 0
        if utils.sim_check_for_empty(string1, string2):
            return 0

        return affine(string1, string2, self.gap_start, self.gap_continuation, self.sim_func)

    def get_gap_start(self):
        """Get gap start cost.

        Returns:
            gap start cost (float).
        """
        return self.gap_start

    def get_gap_continuation(self):
        """Get gap continuation cost.

        Returns:
            gap continuation cost (float).
        """
        return self.gap_continuation

    def get_sim_func(self):
        """Get similarity function.

        Returns:
            similarity function (function).
        """
        return self.sim_func

    def set_gap_start(self, gap_start):
        """Set gap start cost.

        Args:
            gap_start (float): Cost for the gap at the start.
        """
        self.gap_start = gap_start
        return True

    def set_gap_continuation(self, gap_continuation):
        """Set gap continuation cost.

        Args:
            gap_continuation (float): Cost for the gap continuation.
        """
        self.gap_continuation = gap_continuation
        return True

    def set_sim_func(self, sim_func):
        """Set similarity function.

        Args:
            sim_func (function): Function computing similarity score between two characters, represented as strings.
        """
        self.sim_func = sim_func
        return True
