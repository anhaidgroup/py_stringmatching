from __future__ import division

from py_stringmatching.similarity_measure.sequence_similarity_measure import \
    SequenceSimilarityMeasure


class Ratio(SequenceSimilarityMeasure):
    def __init__(self):
        pass

    def get_raw_score(self, string1, string2):
        # should return 0-100
        pass

    def get_sim_score(self, string1, string2):
        # should return 0-1
        pass
