# Write the benchmarking functions here.
# See "Writing benchmarks" in the asv docs for more information.

from py_stringmatching import simfunctions
from . import _short_string_1, _long_string_1, _medium_string_1, _short_string_2, _long_string_2, _medium_string_2
from . import _small_num_tokens_wi_rep, _small_num_tokens_wo_rep, _med_num_tokens_wi_rep, _med_num_tokens_wo_rep, \
    _large_num_tokens_wi_rep, _large_num_tokens_wo_rep, _long_hamm_string1, _long_hamm_string2


class TimeAffine:
    def time_short_short(self):
        simfunctions.affine(_short_string_1, _short_string_2)

    def time_medium_medium(self):
        simfunctions.affine(_medium_string_1, _medium_string_2)

    def time_long_long(self):
        simfunctions.affine(_long_string_1, _long_string_2)

    def time_short_medium(self):
        simfunctions.affine(_short_string_1, _medium_string_1)

    def time_short_long(self):
        simfunctions.affine(_short_string_1, _long_string_1)

    def time_medium_long(self):
        simfunctions.affine(_medium_string_1, _long_string_1)


class TimeJaro:
    def time_short_short(self):
        simfunctions.jaro(_short_string_1, _short_string_2)

    def time_medium_medium(self):
        simfunctions.jaro(_medium_string_1, _medium_string_2)

    def time_long_long(self):
        simfunctions.jaro(_long_string_1, _long_string_2)

    def time_short_medium(self):
        simfunctions.jaro(_short_string_1, _medium_string_1)

    def time_short_long(self):
        simfunctions.jaro(_short_string_1, _long_string_1)

    def time_medium_long(self):
        simfunctions.jaro(_medium_string_1, _long_string_1)


class TimeJaroWinkler:
    def time_short_short(self):
        simfunctions.jaro_winkler(_short_string_1, _short_string_2)

    def time_medium_medium(self):
        simfunctions.jaro_winkler(_medium_string_1, _medium_string_2)

    def time_long_long(self):
        simfunctions.jaro_winkler(_long_string_1, _long_string_2)

    def time_short_medium(self):
        simfunctions.jaro_winkler(_short_string_1, _medium_string_1)

    def time_short_long(self):
        simfunctions.jaro_winkler(_short_string_1, _long_string_1)

    def time_medium_long(self):
        simfunctions.jaro_winkler(_medium_string_1, _long_string_1)


class TimeHammingDistance:
    def time_short_short(self):
        simfunctions.hamming_distance(_short_string_1, _short_string_1)

    def time_medium_medium(self):
        simfunctions.hamming_distance(_medium_string_1, _medium_string_1)

    def time_long_long(self):
        simfunctions.hamming_distance(_long_hamm_string1, _long_hamm_string2)

        # def time_short_medium(self):
        #     simfunctions.hamming_distance(_short_string_1, _medium_string_1)
        #
        # def time_short_long(self):
        #     simfunctions.hamming_distance(_short_string_1, _long_string_1)
        #
        # def time_medium_long(self):
        #     simfunctions.hamming_distance(_medium_string_1, _long_string_1)


#
# class TimeJaro1:
#     def time_short_short(self):
#         Levenshtein.jaro(_short_string_1, _short_string_2)
#
#     def time_medium_medium(self):
#         Levenshtein.jaro(_medium_string_1, _medium_string_2)
#
#     def time_long_long(self):
#         Levenshtein.jaro(_long_string_1, _long_string_2)
#
#     def time_short_medium(self):
#         Levenshtein.jaro(_short_string_1, _medium_string_1)
#
#     def time_short_long(self):
#         Levenshtein.jaro(_short_string_1, _long_string_1)
#
#     def time_medium_long(self):
#         Levenshtein.jaro(_medium_string_1, _long_string_1)
#
#
class TimeLevenshtein:
    def time_short_short(self):
        simfunctions.levenshtein(_short_string_1, _short_string_2)

    def time_medium_medium(self):
        simfunctions.levenshtein(_medium_string_1, _medium_string_2)

    def time_long_long(self):
        simfunctions.levenshtein(_long_string_1, _long_string_2)

    def time_short_medium(self):
        simfunctions.levenshtein(_short_string_1, _medium_string_1)

    def time_short_long(self):
        simfunctions.levenshtein(_short_string_1, _long_string_1)

    def time_medium_long(self):
        simfunctions.levenshtein(_medium_string_1, _long_string_1)


class TimeBagDistance:
    def time_short_short(self):
        simfunctions.bag_distance(_short_string_1, _short_string_2)

    def time_medium_medium(self):
        simfunctions.bag_distance(_medium_string_1, _medium_string_2)

    def time_long_long(self):
        simfunctions.bag_distance(_long_string_1, _long_string_2)

    def time_short_medium(self):
        simfunctions.bag_distance(_short_string_1, _medium_string_1)

    def time_short_long(self):
        simfunctions.bag_distance(_short_string_1, _long_string_1)

    def time_medium_long(self):
        simfunctions.bag_distance(_medium_string_1, _long_string_1)


class TimeNeedlemanWunsch:
    def time_short_short(self):
        simfunctions.needleman_wunsch(_short_string_1, _short_string_2)

    def time_medium_medium(self):
        simfunctions.needleman_wunsch(_medium_string_1, _medium_string_2)

    def time_long_long(self):
        simfunctions.needleman_wunsch(_long_string_1, _long_string_2)

    def time_short_medium(self):
        simfunctions.needleman_wunsch(_short_string_1, _medium_string_1)

    def time_short_long(self):
        simfunctions.needleman_wunsch(_short_string_1, _long_string_1)

    def time_medium_long(self):
        simfunctions.needleman_wunsch(_medium_string_1, _long_string_1)


class TimeSmithWaterman:
    def time_short_short(self):
        simfunctions.smith_waterman(_short_string_1, _short_string_2)

    def time_medium_medium(self):
        simfunctions.smith_waterman(_medium_string_1, _medium_string_2)

    def time_long_long(self):
        simfunctions.smith_waterman(_long_string_1, _long_string_2)

    def time_short_medium(self):
        simfunctions.smith_waterman(_short_string_1, _medium_string_1)

    def time_short_long(self):
        simfunctions.smith_waterman(_short_string_1, _long_string_1)

    def time_medium_long(self):
        simfunctions.smith_waterman(_medium_string_1, _long_string_1)


class TimeCosine:
    def time_small_small_wo_rep(self):
        simfunctions.cosine(_small_num_tokens_wo_rep, _small_num_tokens_wo_rep)

    def time_small_small_wi_rep(self):
        simfunctions.cosine(_small_num_tokens_wi_rep, _small_num_tokens_wi_rep)

    def time_medium_medium_wo_rep(self):
        simfunctions.cosine(_med_num_tokens_wo_rep, _med_num_tokens_wo_rep)

    def time_medium_medium_wi_rep(self):
        simfunctions.cosine(_med_num_tokens_wi_rep, _med_num_tokens_wi_rep)

    def time_large_large_wo_rep(self):
        simfunctions.cosine(_large_num_tokens_wo_rep, _large_num_tokens_wo_rep)

    def time_large_large_wi_rep(self):
        simfunctions.cosine(_large_num_tokens_wi_rep, _large_num_tokens_wi_rep)

    def time_small_medium_wo_rep(self):
        simfunctions.cosine(_small_num_tokens_wo_rep, _med_num_tokens_wo_rep)

    def time_small_medium_wi_rep(self):
        simfunctions.cosine(_small_num_tokens_wi_rep, _med_num_tokens_wi_rep)

    def time_small_large_wo_rep(self):
        simfunctions.cosine(_small_num_tokens_wo_rep, _large_num_tokens_wo_rep)

    def time_small_large_wi_rep(self):
        simfunctions.cosine(_small_num_tokens_wi_rep, _large_num_tokens_wi_rep)

    def time_medium_large_wo_rep(self):
        simfunctions.cosine(_med_num_tokens_wo_rep, _large_num_tokens_wo_rep)

    def time_medium_large_wi_rep(self):
        simfunctions.cosine(_med_num_tokens_wo_rep, _large_num_tokens_wo_rep)


class TimeJaccard:
    def time_small_small_wo_rep(self):
        simfunctions.jaccard(_small_num_tokens_wo_rep, _small_num_tokens_wo_rep)

    def time_small_small_wi_rep(self):
        simfunctions.jaccard(_small_num_tokens_wi_rep, _small_num_tokens_wi_rep)

    def time_medium_medium_wo_rep(self):
        simfunctions.jaccard(_med_num_tokens_wo_rep, _med_num_tokens_wo_rep)

    def time_medium_medium_wi_rep(self):
        simfunctions.jaccard(_med_num_tokens_wi_rep, _med_num_tokens_wi_rep)

    def time_large_large_wo_rep(self):
        simfunctions.jaccard(_large_num_tokens_wo_rep, _large_num_tokens_wo_rep)

    def time_large_large_wi_rep(self):
        simfunctions.jaccard(_large_num_tokens_wi_rep, _large_num_tokens_wi_rep)

    def time_small_medium_wo_rep(self):
        simfunctions.jaccard(_small_num_tokens_wo_rep, _med_num_tokens_wo_rep)

    def time_small_medium_wi_rep(self):
        simfunctions.jaccard(_small_num_tokens_wi_rep, _med_num_tokens_wi_rep)

    def time_small_large_wo_rep(self):
        simfunctions.jaccard(_small_num_tokens_wo_rep, _large_num_tokens_wo_rep)

    def time_small_large_wi_rep(self):
        simfunctions.jaccard(_small_num_tokens_wi_rep, _large_num_tokens_wi_rep)

    def time_medium_large_wo_rep(self):
        simfunctions.jaccard(_med_num_tokens_wo_rep, _large_num_tokens_wo_rep)

    def time_medium_large_wi_rep(self):
        simfunctions.jaccard(_med_num_tokens_wo_rep, _large_num_tokens_wo_rep)


class TimeOverlap:
    def time_small_small_wo_rep(self):
        simfunctions.overlap_coefficient(_small_num_tokens_wo_rep, _small_num_tokens_wo_rep)

    def time_small_small_wi_rep(self):
        simfunctions.overlap_coefficient(_small_num_tokens_wi_rep, _small_num_tokens_wi_rep)

    def time_medium_medium_wo_rep(self):
        simfunctions.overlap_coefficient(_med_num_tokens_wo_rep, _med_num_tokens_wo_rep)

    def time_medium_medium_wi_rep(self):
        simfunctions.overlap_coefficient(_med_num_tokens_wi_rep, _med_num_tokens_wi_rep)

    def time_large_large_wo_rep(self):
        simfunctions.overlap_coefficient(_large_num_tokens_wo_rep, _large_num_tokens_wo_rep)

    def time_large_large_wi_rep(self):
        simfunctions.overlap_coefficient(_large_num_tokens_wi_rep, _large_num_tokens_wi_rep)

    def time_small_medium_wo_rep(self):
        simfunctions.overlap_coefficient(_small_num_tokens_wo_rep, _med_num_tokens_wo_rep)

    def time_small_medium_wi_rep(self):
        simfunctions.overlap_coefficient(_small_num_tokens_wi_rep, _med_num_tokens_wi_rep)

    def time_small_large_wo_rep(self):
        simfunctions.overlap_coefficient(_small_num_tokens_wo_rep, _large_num_tokens_wo_rep)

    def time_small_large_wi_rep(self):
        simfunctions.overlap_coefficient(_small_num_tokens_wi_rep, _large_num_tokens_wi_rep)

    def time_medium_large_wo_rep(self):
        simfunctions.overlap_coefficient(_med_num_tokens_wo_rep, _large_num_tokens_wo_rep)

    def time_medium_large_wi_rep(self):
        simfunctions.overlap_coefficient(_med_num_tokens_wo_rep, _large_num_tokens_wo_rep)


class TimeMongeElkan:
    def time_small_small_wo_rep(self):
        simfunctions.monge_elkan(_small_num_tokens_wo_rep, _small_num_tokens_wo_rep)

    def time_small_small_wi_rep(self):
        simfunctions.monge_elkan(_small_num_tokens_wi_rep, _small_num_tokens_wi_rep)

    def time_medium_medium_wo_rep(self):
        simfunctions.monge_elkan(_med_num_tokens_wo_rep, _med_num_tokens_wo_rep)

    def time_medium_medium_wi_rep(self):
        simfunctions.monge_elkan(_med_num_tokens_wi_rep, _med_num_tokens_wi_rep)

    def time_large_large_wo_rep(self):
        simfunctions.monge_elkan(_large_num_tokens_wo_rep, _large_num_tokens_wo_rep)

    def time_large_large_wi_rep(self):
        simfunctions.monge_elkan(_large_num_tokens_wi_rep, _large_num_tokens_wi_rep)

    def time_small_medium_wo_rep(self):
        simfunctions.monge_elkan(_small_num_tokens_wo_rep, _med_num_tokens_wo_rep)

    def time_small_medium_wi_rep(self):
        simfunctions.monge_elkan(_small_num_tokens_wi_rep, _med_num_tokens_wi_rep)


class TimeTfIdf:
    corpus_list = [_small_num_tokens_wo_rep, _small_num_tokens_wi_rep, _med_num_tokens_wi_rep, _med_num_tokens_wo_rep,
                   _large_num_tokens_wo_rep, _large_num_tokens_wi_rep]

    def time_small_small_wo_rep_no_corpus_no_dampen(self):
        simfunctions.tfidf(_small_num_tokens_wo_rep, _small_num_tokens_wo_rep)

    def time_small_small_wi_rep_no_corpus_no_dampen(self):
        simfunctions.tfidf(_small_num_tokens_wi_rep, _small_num_tokens_wi_rep)

    def time_medium_medium_wo_rep_no_corpus_no_dampen(self):
        simfunctions.tfidf(_med_num_tokens_wo_rep, _med_num_tokens_wo_rep)

    def time_medium_medium_wi_rep_no_corpus_no_dampen(self):
        simfunctions.tfidf(_med_num_tokens_wi_rep, _med_num_tokens_wi_rep)

    def time_large_large_wo_rep_no_corpus_no_dampen(self):
        simfunctions.tfidf(_large_num_tokens_wo_rep, _large_num_tokens_wo_rep)

    def time_large_large_wi_rep_no_corpus_no_dampen(self):
        simfunctions.tfidf(_large_num_tokens_wi_rep, _large_num_tokens_wi_rep)

    def time_small_medium_wo_rep_no_corpus_no_dampen(self):
        simfunctions.tfidf(_small_num_tokens_wo_rep, _med_num_tokens_wo_rep)

    def time_small_medium_wi_rep_no_corpus_no_dampen(self):
        simfunctions.tfidf(_small_num_tokens_wi_rep, _med_num_tokens_wi_rep)

    def time_small_large_wo_rep_no_corpus_no_dampen(self):
        simfunctions.tfidf(_small_num_tokens_wo_rep, _large_num_tokens_wo_rep)

    def time_small_large_wi_rep_no_corpus_no_dampen(self):
        simfunctions.tfidf(_small_num_tokens_wi_rep, _large_num_tokens_wi_rep)

    def time_medium_large_wo_rep_no_corpus_no_dampen(self):
        simfunctions.tfidf(_med_num_tokens_wo_rep, _large_num_tokens_wo_rep)

    def time_medium_large_wi_rep_no_corpus_no_dampen(self):
        simfunctions.tfidf(_med_num_tokens_wo_rep, _large_num_tokens_wo_rep)

    # dampen - true
    def time_small_small_wo_rep_no_corpus(self):
        simfunctions.tfidf(_small_num_tokens_wo_rep, _small_num_tokens_wo_rep, dampen=True)

    def time_small_small_wi_rep_no_corpus(self):
        simfunctions.tfidf(_small_num_tokens_wi_rep, _small_num_tokens_wi_rep, dampen=True)

    def time_medium_medium_wo_rep_no_corpus(self):
        simfunctions.tfidf(_med_num_tokens_wo_rep, _med_num_tokens_wo_rep, dampen=True)

    def time_medium_medium_wi_rep_no_corpus(self):
        simfunctions.tfidf(_med_num_tokens_wi_rep, _med_num_tokens_wi_rep, dampen=True)

    def time_large_large_wo_rep_no_corpus(self):
        simfunctions.tfidf(_large_num_tokens_wo_rep, _large_num_tokens_wo_rep, dampen=True)

    def time_large_large_wi_rep_no_corpus(self):
        simfunctions.tfidf(_large_num_tokens_wi_rep, _large_num_tokens_wi_rep, dampen=True)

    def time_small_medium_wo_rep_no_corpus(self):
        simfunctions.tfidf(_small_num_tokens_wo_rep, _med_num_tokens_wo_rep, dampen=True)

    def time_small_medium_wi_rep_no_corpus(self):
        simfunctions.tfidf(_small_num_tokens_wi_rep, _med_num_tokens_wi_rep, dampen=True)

    def time_small_large_wo_rep_no_corpus(self):
        simfunctions.tfidf(_small_num_tokens_wo_rep, _large_num_tokens_wo_rep, dampen=True)

    def time_small_large_wi_rep_no_corpus(self):
        simfunctions.tfidf(_small_num_tokens_wi_rep, _large_num_tokens_wi_rep, dampen=True)

    def time_medium_large_wo_rep_no_corpus(self):
        simfunctions.tfidf(_med_num_tokens_wo_rep, _large_num_tokens_wo_rep, dampen=True)

    def time_medium_large_wi_rep_no_corpus(self):
        simfunctions.tfidf(_med_num_tokens_wo_rep, _large_num_tokens_wo_rep, dampen=True)

    # corpus list - true
    def time_small_small_wo_rep_no_dampen(self):
        simfunctions.tfidf(_small_num_tokens_wo_rep, _small_num_tokens_wo_rep, corpus_list=self.corpus_list)

    def time_small_small_wi_rep_no_dampen(self):
        simfunctions.tfidf(_small_num_tokens_wi_rep, _small_num_tokens_wi_rep, corpus_list=self.corpus_list)

    def time_medium_medium_wo_rep_no_dampen(self):
        simfunctions.tfidf(_med_num_tokens_wo_rep, _med_num_tokens_wo_rep, corpus_list=self.corpus_list)

    def time_medium_medium_wi_rep_no_dampen(self):
        simfunctions.tfidf(_med_num_tokens_wi_rep, _med_num_tokens_wi_rep, corpus_list=self.corpus_list)

    def time_large_large_wo_rep_no_dampen(self):
        simfunctions.tfidf(_large_num_tokens_wo_rep, _large_num_tokens_wo_rep, corpus_list=self.corpus_list)

    def time_large_large_wi_rep_no_dampen(self):
        simfunctions.tfidf(_large_num_tokens_wi_rep, _large_num_tokens_wi_rep, corpus_list=self.corpus_list)

    def time_small_medium_wo_rep_no_dampen(self):
        simfunctions.tfidf(_small_num_tokens_wo_rep, _med_num_tokens_wo_rep, corpus_list=self.corpus_list)

    def time_small_medium_wi_rep_no_dampen(self):
        simfunctions.tfidf(_small_num_tokens_wi_rep, _med_num_tokens_wi_rep, corpus_list=self.corpus_list)

    def time_small_large_wo_rep_no_dampen(self):
        simfunctions.tfidf(_small_num_tokens_wo_rep, _large_num_tokens_wo_rep, corpus_list=self.corpus_list)

    def time_small_large_wi_rep_no_dampen(self):
        simfunctions.tfidf(_small_num_tokens_wi_rep, _large_num_tokens_wi_rep, corpus_list=self.corpus_list)

    def time_medium_large_wo_rep_no_dampen(self):
        simfunctions.tfidf(_med_num_tokens_wo_rep, _large_num_tokens_wo_rep, corpus_list=self.corpus_list)

    def time_medium_large_wi_rep_no_dampen(self):
        simfunctions.tfidf(_med_num_tokens_wo_rep, _large_num_tokens_wo_rep, corpus_list=self.corpus_list)

    # corpus list - true, dampen_true
    def time_small_small_wo_rep(self):
        simfunctions.tfidf(_small_num_tokens_wo_rep, _small_num_tokens_wo_rep, corpus_list=self.corpus_list,
                           dampen=True)

    def time_small_small_wi_rep(self):
        simfunctions.tfidf(_small_num_tokens_wi_rep, _small_num_tokens_wi_rep, corpus_list=self.corpus_list,
                           dampen=True)

    def time_medium_medium_wo_rep(self):
        simfunctions.tfidf(_med_num_tokens_wo_rep, _med_num_tokens_wo_rep, corpus_list=self.corpus_list,
                           dampen=True)

    def time_medium_medium_wi_rep(self):
        simfunctions.tfidf(_med_num_tokens_wi_rep, _med_num_tokens_wi_rep, corpus_list=self.corpus_list,
                           dampen=True)

    def time_large_large_wo_rep(self):
        simfunctions.tfidf(_large_num_tokens_wo_rep, _large_num_tokens_wo_rep, corpus_list=self.corpus_list,
                           dampen=True)

    def time_large_large_wi_rep(self):
        simfunctions.tfidf(_large_num_tokens_wi_rep, _large_num_tokens_wi_rep, corpus_list=self.corpus_list,
                           dampen=True)

    def time_small_medium_wo_rep(self):
        simfunctions.tfidf(_small_num_tokens_wo_rep, _med_num_tokens_wo_rep, corpus_list=self.corpus_list, dampen=True)

    def time_small_medium_wi_rep(self):
        simfunctions.tfidf(_small_num_tokens_wi_rep, _med_num_tokens_wi_rep, corpus_list=self.corpus_list, dampen=True)

    def time_small_large_wo_rep(self):
        simfunctions.tfidf(_small_num_tokens_wo_rep, _large_num_tokens_wo_rep, corpus_list=self.corpus_list,
                           dampen=True)

    def time_small_large_wi_rep(self):
        simfunctions.tfidf(_small_num_tokens_wi_rep, _large_num_tokens_wi_rep, corpus_list=self.corpus_list,
                           dampen=True)

    def time_medium_large_wo_rep(self):
        simfunctions.tfidf(_med_num_tokens_wo_rep, _large_num_tokens_wo_rep, corpus_list=self.corpus_list, dampen=True)

    def time_medium_large_wi_rep(self):
        simfunctions.tfidf(_med_num_tokens_wo_rep, _large_num_tokens_wo_rep, corpus_list=self.corpus_list, dampen=True)


class TimeSoftTfIdf:
    corpus_list = [_small_num_tokens_wo_rep, _small_num_tokens_wi_rep, _med_num_tokens_wi_rep, _med_num_tokens_wo_rep,
                   _large_num_tokens_wo_rep, _large_num_tokens_wi_rep]

    # no corpus list
    def time_small_small_wo_rep_no_corpus(self):
        simfunctions.soft_tfidf(_small_num_tokens_wo_rep, _small_num_tokens_wo_rep)

    def time_small_small_wi_rep_no_corpus(self):
        simfunctions.soft_tfidf(_small_num_tokens_wi_rep, _small_num_tokens_wi_rep)

    def time_medium_medium_wo_rep_no_corpus(self):
        simfunctions.soft_tfidf(_med_num_tokens_wo_rep, _med_num_tokens_wo_rep)

    def time_medium_medium_wi_rep_no_corpus(self):
        simfunctions.soft_tfidf(_med_num_tokens_wi_rep, _med_num_tokens_wi_rep)

    def time_large_large_wo_rep_no_corpus(self):
        simfunctions.soft_tfidf(_large_num_tokens_wo_rep, _large_num_tokens_wo_rep)

    def time_large_large_wi_rep_no_corpus(self):
        simfunctions.soft_tfidf(_large_num_tokens_wi_rep, _large_num_tokens_wi_rep)

    def time_small_medium_wo_rep_no_corpus(self):
        simfunctions.soft_tfidf(_small_num_tokens_wo_rep, _med_num_tokens_wo_rep)

    def time_small_medium_wi_rep_no_corpus(self):
        simfunctions.soft_tfidf(_small_num_tokens_wi_rep, _med_num_tokens_wi_rep)

    def time_small_large_wo_rep_no_corpus(self):
        simfunctions.soft_tfidf(_small_num_tokens_wo_rep, _large_num_tokens_wo_rep)

    def time_small_large_wi_rep_no_corpus(self):
        simfunctions.soft_tfidf(_small_num_tokens_wi_rep, _large_num_tokens_wi_rep)

    def time_medium_large_wo_rep_no_corpus(self):
        simfunctions.soft_tfidf(_med_num_tokens_wo_rep, _large_num_tokens_wo_rep)

    def time_medium_large_wi_rep_no_corpus(self):
        simfunctions.soft_tfidf(_med_num_tokens_wo_rep, _large_num_tokens_wo_rep)

    # with corpus list
    def time_small_small_wo_rep(self):
        simfunctions.soft_tfidf(_small_num_tokens_wo_rep, _small_num_tokens_wo_rep, corpus_list=self.corpus_list)

    def time_small_small_wi_rep(self):
        simfunctions.soft_tfidf(_small_num_tokens_wi_rep, _small_num_tokens_wi_rep, corpus_list=self.corpus_list)

    def time_medium_medium_wo_rep(self):
        simfunctions.soft_tfidf(_med_num_tokens_wo_rep, _med_num_tokens_wo_rep, corpus_list=self.corpus_list)

    def time_medium_medium_wi_rep(self):
        simfunctions.soft_tfidf(_med_num_tokens_wi_rep, _med_num_tokens_wi_rep, corpus_list=self.corpus_list)

    def time_large_large_wo_rep(self):
        simfunctions.soft_tfidf(_large_num_tokens_wo_rep, _large_num_tokens_wo_rep, corpus_list=self.corpus_list)

    def time_large_large_wi_rep(self):
        simfunctions.soft_tfidf(_large_num_tokens_wi_rep, _large_num_tokens_wi_rep, corpus_list=self.corpus_list)

    def time_small_medium_wo_rep(self):
        simfunctions.soft_tfidf(_small_num_tokens_wo_rep, _med_num_tokens_wo_rep, corpus_list=self.corpus_list)

    def time_small_medium_wi_rep(self):
        simfunctions.soft_tfidf(_small_num_tokens_wi_rep, _med_num_tokens_wi_rep, corpus_list=self.corpus_list)

    def time_small_large_wo_rep(self):
        simfunctions.soft_tfidf(_small_num_tokens_wo_rep, _large_num_tokens_wo_rep, corpus_list=self.corpus_list)

    def time_small_large_wi_rep(self):
        simfunctions.soft_tfidf(_small_num_tokens_wi_rep, _large_num_tokens_wi_rep, corpus_list=self.corpus_list)

    def time_medium_large_wo_rep(self):
        simfunctions.soft_tfidf(_med_num_tokens_wo_rep, _large_num_tokens_wo_rep, corpus_list=self.corpus_list)

    def time_medium_large_wi_rep(self):
        simfunctions.soft_tfidf(_med_num_tokens_wo_rep, _large_num_tokens_wo_rep, corpus_list=self.corpus_list)
