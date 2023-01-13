# cython: boundscheck=False

from __future__ import division
import cython
import numpy as np
cimport numpy as np
from py_stringmatching.similarity_measure.cython.cython_utils import int_min_three
from numpy import int32
from numpy cimport int32_t

DTYPE = int
ctypedef np.int_t DTYPE_t

@cython.boundscheck(False)
@cython.wraparound(False)



def levenshtein(unicode string1, unicode string2):

    cdef int len_str1 = len(string1)
    cdef int len_str2 = len(string2)

    cdef int ins_cost = 1
    cdef int del_cost = 1
    cdef int sub_cost = 1
    cdef int trans_cost = 1

    cdef int i = 0
    cdef int j = 0

    if len_str1 == 0:
        return len_str2 * ins_cost

    if len_str2 == 0:
        return len_str1 * del_cost

    cdef int[:,:] d_mat = np.zeros((len_str1 + 1, len_str2 + 1), dtype=np.int32)

    for i from 0 <= i < (len_str1 + 1):
        d_mat[i, 0] = i * del_cost

    for j from 0 <= j < (len_str2 + 1):
        d_mat[0, j] = j * ins_cost

    cdef unsigned char lchar = 0
    cdef unsigned char rchar = 0

    for i from 0 <= i < (len_str1):
        lchar = string1[i]
        for j from 0 <= j < (len_str2):
            rchar = string2[j]

            d_mat[i+1,j+1] = int_min_three(d_mat[i + 1, j] + ins_cost, d_mat[i, j + 1] + del_cost, d_mat[i, j]
                                        + (sub_cost if lchar != rchar else 0))
    return d_mat[len_str1, len_str2]
