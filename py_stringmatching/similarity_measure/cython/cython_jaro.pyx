# coding=utf-8
# from __future__ import division
import cython
cimport cython

import numpy as np
cimport numpy as np

#Cython functions to compute the Jaro score

cdef inline int int_max(int a,int b):
    """Finds the maximum integer of the given two integers.

        Args:
            integer1,integer2 (int): Input integers.

        Returns:
            Maximum integer (int).

    """
    if a > b : return a
    else: return b

def jaro(unicode string1, unicode string2):
    """Computes the Jaro score between two strings.

        Args:
            string1,string2 (str): Input strings.

        Returns:
            Jaro distance score (float).


    """

    cdef int i=0
    cdef int j=0

    cdef int len_str1 = len(string1)
    cdef int len_str2 = len(string2)
    cdef int max_len = int_max(len_str1, len_str2)
    cdef int search_range = (max_len // 2) - 1

    if search_range<0:
        search_range=0

    # populating numpy arrays of length as each string with zeros
    cdef int[:] flags_s1 = np.zeros(len_str1,dtype=np.int32)
    cdef int[:] flags_s2 = np.zeros(len_str2,dtype=np.int32)

    cdef int common_chars = 0
    cdef int low=0
    cdef int high=0

    # Finding the number of common characters in two strings
    for i from 0<= i < len_str1:
        low = i - search_range if i > search_range else 0
        high = i + search_range if i + search_range < len_str2 else len_str2 - 1
        for j from low <= j < (high + 1):
            if (flags_s2[j]==0) and (string2[j] == string1[i]):
                flags_s1[i] = flags_s2[j] = 1
                common_chars += 1
                break

    if common_chars==0:
        return 0

    cdef int k = 0
    trans_count = 0

    # Finding the number of transpositions and Jaro distance
    for i from 0<= i < len_str1:
        if (flags_s1[i]==1):
            for j from k<= j < len_str2:
                if (flags_s2[j]==1):
                    k = j + 1
                    break
            if string1[i] != string2[j]:
                trans_count += 1
    trans_count /= 2
    cdef float weight = (float(common_chars) / len_str1 + float(common_chars) / len_str2 +
                         (float(common_chars) - trans_count) / float(common_chars)) / 3
    return weight




