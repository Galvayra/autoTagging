#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import OrderedDict

# If you want to build preprocessing.py, set True
IS_PRE_PROCESSING = False

# If you want to build filling.py which target is target csv file tagged automatically, set True
IS_STEP_TO_MAKE_FULL_DICT = True

columns = OrderedDict()
columns['name'] = 'Filename'
columns['start'] = 'Start Speech'
columns['end'] = 'End Speech'
columns['data'] = 'Ground Truth Script'
columns['keyword'] = 'Keyword'
columns['ontology'] = 'Ontology'
columns['category'] = 'Category'
columns['pos'] = 'Keyword(POS, 정규화 과정)'

origin_dir_path = "KIST/"

# # Dataset path
dictionary_path = "Dataset/"
dictionary_csv = "final_manual.csv"
target_csv = "final_target.csv"
test_csv = "final_test.csv"
test_manual_csv = "final_manual_test.csv"

if IS_STEP_TO_MAKE_FULL_DICT:
	full_ = "full_"
	dictionary_csv = "auto_final_target.csv"
else:
	full_ = ""

similar_tbl = "similar_tbl"
dictionary_save = full_ + "dict"
similar_save = full_ + "similar_dict"
conversation_save = full_ + "conversation_dict"
overlap_keyword_file = "overlap_keywords"
# #

# # speech path
speech_file_path = "FinalSpeechData/"
# #

# # Feature

feature_path = "Word2Vec/"
w2v_file_name = "total_w2v"
feature_overlap_save = full_ + "features_overlap"
feature_not_verb_save = full_ + "features_not_verb"
feature_verb_save = full_ + "features_verb"
feature_similar_save = full_ + "features_similar"
# #

key_conversation = "conversation"
key_overlap = "overlap"
key_n_verb = "not_verb"
key_y_verb = "verb"
key_similar = "similar"

key_ontology = "ontology"
key_vector = "vector"
