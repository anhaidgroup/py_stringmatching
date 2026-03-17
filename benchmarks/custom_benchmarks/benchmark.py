# -*- coding: utf-8 -*-
import timeit


class Benchmark:

    def __init__(self, bm_pairs=1.0):
        """Default value for bm_pairs
         bm_pairs = 1
        """
        self.bm_pairs = bm_pairs

    def get_benchmark(self, measure, set1, set2):
        """ To get the total runtime for the string matching operation on given sets of strings.
        Args:
            measure (function): Similarity measure to be benchmarked.
            set1, set2 (Set): input sets to compare the strings and get the score.
        Return:
            Total runtime to do the string matching operation in seconds.

        """
        result = []
        bm_result = []
        start = timeit.default_timer()

        if len(set1) > len(set2):
            max_len = len(set2)
        else:
            max_len = len(set1)

        if self.bm_pairs != 1:
            min_len = self.bm_pairs
            for m in range(max_len):
                for n in range(min_len):
                    score = measure.get_raw_score(str(set1[m]), str(set2[n]))
                    result.append(score)
            stop = timeit.default_timer()
            bm = stop - start
            bm_result.append(bm)
            return bm_result
        else:
            for m in range(max_len):
                score = measure.get_raw_score(str(set1[m]), str(set2[m]))
                result.append(score)
            stop = timeit.default_timer()
            bm = stop - start
            bm_result.append(bm)
            return bm_result

    def set_bm_pairs(self, bm_pairs):
        """Set benchmark pairs.
            If bm_pairs = 1 then the benchmark is for string-string pairs
            if bm_pairs > 1 then the benchmark is for the cartesian products between
            each string in setA and benchmark pairs in setB

        Args:
            bm_pairs (int): number of pairs with each string.
        """
        self.bm_pairs = bm_pairs
        return True


