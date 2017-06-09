# -*- coding: utf-8 -*-


import timeit


class benchmark():

    def __init__(self, bm_pairs=1.0):
        self.bm_pairs = bm_pairs

    def get_benchmark(self, measure,setA, setB):

        # print(measure.get_raw_score('Nóáll','Neál'))
        result = []
        bm_result = []
        start = timeit.default_timer()
        if (len(setA) > len(setB)):
            maxlen = len(setB)
        else:
            maxlen = len(setA)

        if (self.bm_pairs != 1):
            minlen = self.bm_pairs
            for m in range(maxlen):
                for n in range(minlen):
                    score = measure.get_raw_score(str(setA[m]), str(setB[n]))
                    result.append(score)
            stop = timeit.default_timer()
            bm = stop - start
            bm_result.append(bm)
            # print(result)
            # print(bm_result)
            return bm_result
        else:
            for m in range(maxlen):
                score = measure.get_raw_score(str(setA[m]), str(setB[m]))
                result.append(score)
            stop = timeit.default_timer()
            bm = stop - start
            bm_result.append(bm)
            # print(bm_result)
            # print(result)
            return bm_result

    def set_bm_pairs(self, bm_pairs):
        """Set benchmark pairs.
            If benchmark pairs = 1 then the benchmark is for string pairs
            if benchmark pairs > 1 then the benchmark is for the cartesian products between
            each string in setA and benchmark pairs in setB

        Args:
            bm_pairs (int): number of pairs with each string.
        """
        self.bm_pairs = bm_pairs
        return True


