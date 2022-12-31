import cython
import numpy as np
cimport numpy as np

@cython.boundscheck(False)
@cython.wraparound(False)

def needleman_wunsch(unicode string1, unicode string2, float gap_cost,
                                                            sim_score):
    """ Computes Needleman-Wunsch measure raw score.
    Args:
        string1, string2 (unicode): Input unicode strings
        gap_cost (float): Cost of gap
        sim_score (sim function): Similarity function given by user if not use default sim ident function
    Returns:
        Returns Needleman-Wunsch similarity score (float)
    """

    cdef int i = 0, j = 0
    cdef double match = 0.0, delete = 0.0, insert = 0.0
    cdef double sim_func_score = 0.0
    cdef int len_s1 = len(string1), len_s2 = len(string2)
    cdef double[:,:] dist_mat = np.zeros((len(string1) + 1, len(string2) + 1), dtype=float)

    # DP initialization
    for i from 0 <= i < (len_s1 + 1):
        dist_mat[i, 0] = -(i * gap_cost)

    # DP initialization
    for j from 0 <= j < (len_s2 + 1):
        dist_mat[0, j] = -(j * gap_cost)


    # Needleman-Wunsch DP calculation
    for i from 1 <= i < (len_s1 + 1):
        for j from 1 <= j < (len_s2 + 1):
            sim_func_score = sim_score(string1[i - 1], string2[j - 1])
            match = dist_mat[i - 1, j - 1] + sim_func_score
            delete = dist_mat[i - 1, j] - gap_cost
            insert = dist_mat[i, j - 1] - gap_cost
            dist_mat[i, j] = max(match, delete, insert)

    return dist_mat[len_s1, len_s2]