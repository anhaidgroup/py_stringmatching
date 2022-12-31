"""Fuzzy Wuzzy Token Sort Similarity Measure"""

from py_stringmatching import utils

from py_stringmatching.similarity_measure.sequence_similarity_measure import \
                                                    SequenceSimilarityMeasure
from py_stringmatching.similarity_measure.partial_ratio import PartialRatio


class PartialTokenSort(SequenceSimilarityMeasure):
    """Computes Fuzzy Wuzzy partial token sort similarity measure.

    Fuzzy Wuzzy partial token sort ratio raw raw_score is a measure of the strings similarity as an 
    int in the range [0, 100]. For two strings X and Y, the score is obtained by
    splitting the two strings into tokens and then sorting the tokens. The score is
    then the fuzzy wuzzy partial ratio raw score of the transformed strings. Fuzzy Wuzzy token
    sort sim score is a float in the range [0, 1] and is obtained by dividing the raw score
    by 100.
        
     Note:
         In the case where either of strings X or Y are empty, we define the
         Fuzzy Wuzzy partial ratio similarity score to be 0. 
    """
    def __init__(self):
        pass

    def _process_string_and_sort(self, s, force_ascii, full_process=True):
        """Returns a string with tokens sorted. Processes the string if
        full_process flag is enabled. If force_ascii flag is enabled then
        processing removes non ascii characters from the string."""
        # pull tokens
        ts = utils.process_string(s, force_ascii=force_ascii) if full_process else s
        tokens = ts.split()

        # sort tokens and join
        sorted_string = u" ".join(sorted(tokens))
        return sorted_string.strip()

    def get_raw_score(self, string1, string2, force_ascii=True, full_process=True):
        """
        Computes the Fuzzy Wuzzy partial token sort measure raw score between two strings.
        This score is in the range [0,100].

        Args:
            string1,string2 (str), : Input strings
            force_ascii (boolean) : Flag to remove non-ascii characters or not
            full_process (boolean) : Flag to process the string or not. Processing includes
            removing non alphanumeric characters, converting string to lower case and 
            removing leading and trailing whitespaces.

        Returns:
            Partial Token Sort measure raw score (int) is returned

        Raises:
            TypeError: If the inputs are not strings

        Examples:
            >>> s = PartialTokenSort()
            >>> s.get_raw_score('great is scala', 'java is great')
            81
            >>> s.get_raw_score('Sue', 'sue')
            100
            >>> s.get_raw_score('C++ and Java', 'Java and Python')
            64

        References:
            * https://pypi.python.org/pypi/fuzzywuzzy
        """
        # input validations
        utils.sim_check_for_none(string1, string2)
        utils.sim_check_for_string_inputs(string1, string2)

        # if one of the strings is empty return 0
        if utils.sim_check_for_empty(string1, string2):
            return 0

        sorted1 = self._process_string_and_sort(string1, force_ascii, full_process=full_process)
        sorted2 = self._process_string_and_sort(string2, force_ascii, full_process=full_process)
        partialRatio = PartialRatio()
        return partialRatio.get_raw_score(sorted1, sorted2)

    def get_sim_score(self, string1, string2, force_ascii=True, full_process=True):
        """
        Computes the Fuzzy Wuzzy partial token sort similarity score between two strings.
        This score is in the range [0,1].

        Args:
            string1,string2 (str), : Input strings
            force_ascii (boolean) : Flag to remove non-ascii characters or not
            full_process (boolean) : Flag to process the string or not. Processing includes
            removing non alphanumeric characters, converting string to lower case and 
            removing leading and trailing whitespaces.

        Returns:
            Partial Token Sort measure similarity score (float) is returned

        Raises:
            TypeError: If the inputs are not strings

        Examples:
            >>> s = PartialTokenSort()
            >>> s.get_sim_score('great is scala', 'java is great')
            0.81
            >>> s.get_sim_score('Sue', 'sue')
            1.0
            >>> s.get_sim_score('C++ and Java', 'Java and Python')
            0.64

        References:
            * https://pypi.python.org/pypi/fuzzywuzzy
        """
        raw_score = 1.0 * self.get_raw_score(string1, string2, force_ascii, full_process)
        sim_score = raw_score / 100
        return sim_score