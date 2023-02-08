import cython
import numpy as np
cimport numpy as np

@cython.boundscheck(False)
@cython.wraparound(False)


def smith_waterman(unicode string1, unicode string2, float gap_cost, \
                                                             sim_func):

    cdef int i = 0, j = 0
    cdef double match = 0.0, delete = 0.0, insert = 0.0
    cdef double sim_score = 0.0, max_value = 0.0
    cdef int len_s1 = len(string1), len_s2 = len(string2)
    cdef double[:,:] dist_mat = np.zeros((len(string1) + 1, len(string2) + 1), dtype=float)


    # Smith Waterman DP calculations
    for i from 1 <= i < (len_s1 + 1):
        for j from 1 <= j < (len_s2 + 1):

            sim_func_score = sim_func(string1[i - 1], string2[j - 1])
            match = dist_mat[i - 1, j - 1] + sim_func_score
            delete = dist_mat[i - 1, j] - gap_cost
            insert = dist_mat[i, j - 1] - gap_cost
            dist_mat[i, j] = max(0, match, delete, insert)
            max_value = max(max_value, dist_mat[i, j])

    return max_value