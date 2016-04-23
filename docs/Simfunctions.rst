Similarity Functions
====================

.. automodule:: py_stringmatching.simfunctions


.. autofunction:: levenshtein(string1, string2)
.. autofunction:: bag_distance(string1, string2)
.. autofunction:: hamming_distance(string1, string2)
.. autofunction:: jaro(string1, string2)
.. autofunction:: jaro_winkler(string1, string2, prefix_weight=0.1)
.. autofunction:: needleman_wunsch(string1, string2, gap_cost=1, sim_score=sim_ident)
.. autofunction:: smith_waterman(string1, string2, gap_cost=1, sim_score=sim_ident)
.. autofunction:: affine(string1, string2, gap_start=1, gap_continuation=0.5, sim_score=sim_ident)
.. autofunction:: jaccard(set1, set2)
.. autofunction:: overlap_coefficient(set1, set2)
.. autofunction:: cosine(set1, set2)
.. autofunction:: monge_elkan(bag1, bag2, sim_func=levenshtein)
.. autofunction:: tfidf(bag1, bag2, corpus_list = None, dampen=False)
.. autofunction:: soft_tfidf(bag1, bag2, corpus_list=None, sim_func=jaro, threshold=0.5)