from py_stringmatching import utils
from py_stringmatching.similarity_measure.sequence_similarity_measure import \
                                                    SequenceSimilarityMeasure
from py_stringmatching.similarity_measure.cython.cython_jaro import jaro


class Jaro(SequenceSimilarityMeasure):
    """Computes Jaro measure.

    The Jaro measure is a type of edit distance, developed mainly to compare short strings,
    such as first and last names.
    """

    def __init__(self):
        super(Jaro, self).__init__()

    def get_raw_score(self, string1, string2):
        """Computes the raw Jaro score between two strings.

        Args:
            string1,string2 (str): Input strings.

        Returns:
            Jaro similarity score (float).

        Raises:
            TypeError : If the inputs are not strings or if one of the inputs is None.

        Examples:
            >>> jaro = Jaro()
            >>> jaro.get_raw_score('MARTHA', 'MARHTA')
            0.9444444444444445
            >>> jaro.get_raw_score('DWAYNE', 'DUANE')
            0.8222222222222223
            >>> jaro.get_raw_score('DIXON', 'DICKSONX')
            0.7666666666666666

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

        return jaro(string1, string2)

    def get_sim_score(self, string1, string2):
        """Computes the normalized Jaro similarity score between two strings. Simply call get_raw_score.

        Args:
            string1,string2 (str): Input strings.

        Returns:
            Normalized Jaro similarity score (float).

        Raises:
            TypeError : If the inputs are not strings or if one of the inputs is None.

        Examples:
            >>> jaro = Jaro()
            >>> jaro.get_sim_score('MARTHA', 'MARHTA')
            0.9444444444444445
            >>> jaro.get_sim_score('DWAYNE', 'DUANE')
            0.8222222222222223
            >>> jaro.get_sim_score('DIXON', 'DICKSONX')
            0.7666666666666666

        """
        return self.get_raw_score(string1, string2)
