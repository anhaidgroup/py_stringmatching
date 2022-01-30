from py_stringmatching import utils
from py_stringmatching.similarity_measure.jaro_winkler import JaroWinkler
from py_stringmatching.similarity_measure.hybrid_similarity_measure import \
                                                    HybridSimilarityMeasure


class MongeElkan(HybridSimilarityMeasure):
    """Computes Monge-Elkan measure.

    The Monge-Elkan similarity measure is a type of hybrid similarity measure that combines the benefits of
    sequence-based and set-based methods. This can be effective for domains in which more control is needed
    over the similarity measure. It implicitly uses a secondary similarity measure, such as Levenshtein to compute
    over all similarity score. See the string matching chapter in the DI book (Principles of Data Integration). 

    Args:
        sim_func (function): Secondary similarity function. This is expected to be a sequence-based
                             similarity measure (defaults to Jaro-Winkler similarity measure).

    Attributes:
        sim_func (function): An attribute to store the secondary similarity function.
    """

    def __init__(self, sim_func=JaroWinkler().get_raw_score):
        self.sim_func = sim_func
        super(MongeElkan, self).__init__()

    def get_raw_score(self, bag1, bag2):
        """Computes the raw Monge-Elkan score between two bags (lists).

        Args:
            bag1,bag2 (list): Input lists.

        Returns:
            Monge-Elkan similarity score (float).

        Raises:
            TypeError : If the inputs are not lists or if one of the inputs is None.

        Examples:
            >>> me = MongeElkan()
            >>> me.get_raw_score(['Niall'], ['Neal'])
            0.8049999999999999
            >>> me.get_raw_score(['Niall'], ['Nigel'])
            0.7866666666666667
            >>> me.get_raw_score(['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'], ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego'])
            0.8364448130130768
            >>> me.get_raw_score([''], ['a'])
            0.0
            >>> me = MongeElkan(sim_func=NeedlemanWunsch().get_raw_score)
            >>> me.get_raw_score(['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'], ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego'])
            2.0
            >>> me = MongeElkan(sim_func=Affine().get_raw_score)
            >>> me.get_raw_score(['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'], ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego'])
            2.25

        References:
            * Principles of Data Integration book
        """
        
        # input validations
        utils.sim_check_for_none(bag1, bag2)
        utils.sim_check_for_list_or_set_inputs(bag1, bag2)

        # if exact match return 1.0
        if utils.sim_check_for_exact_match(bag1, bag2):
            return 1.0

        # if one of the strings is empty return 0
        if utils.sim_check_for_empty(bag1, bag2):
            return 0

        # aggregated sum of all the max sim score of all the elements in bag1
        # with elements in bag2
        sum_of_maxes = 0
        for el1 in bag1:
            max_sim = float('-inf')
            for el2 in bag2:
                max_sim = max(max_sim, self.sim_func(el1, el2))
            sum_of_maxes += max_sim

        sim = float(sum_of_maxes) / float(len(bag1))

        return sim

    def get_sim_func(self):
        """Get the secondary similarity function.

        Returns:
            secondary similarity function (function).
        """
        return self.sim_func

    def set_sim_func(self, sim_func):
        """Set the secondary similarity function.

        Args:
            sim_func (function): Secondary similarity function.
        """
        self.sim_func = sim_func
        return True
