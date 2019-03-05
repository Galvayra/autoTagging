#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import json
import variables as v
import os
import sys
from Word2Vec.get_vector import get_features, get_vector
from Word2Vec.read_w2v import w2v_dict

TOKEN_VERB = '_'
ONTOLOGY_VERB = "Predicate"
ONTOLOGY_SUBJECT = "Subject"


def set_dicts():
	def save_dict(target_dict, target_path, target_file_name):
		with open(target_path + target_file_name, 'w') as out_file:
			json.dump(target_dict, out_file, ensure_ascii=False, indent=4)

	csv_file = pd.read_csv(v.dictionary_path + v.dictionary_csv)
	print "\n\tRead file -", v.dictionary_path + v.dictionary_csv, "\n"

	ontology_dict = init_ontology_dict(csv_file)
	similar_dict = init_similar_dict(ontology_dict)
	conversation_dict = init_file_dict()
	feature_dicts = init_feature_dicts(csv_file, conversation_dict, ontology_dict, similar_dict)
	vector_dicts = init_vector_dicts(feature_dicts)

	save_dict(target_dict=ontology_dict, target_path=v.dictionary_path, target_file_name=v.dictionary_save)
	save_dict(target_dict=similar_dict, target_path=v.dictionary_path, target_file_name=v.similar_save)
	save_dict(target_dict=conversation_dict, target_path=v.dictionary_path, target_file_name=v.conversation_save)

	save_dict(target_dict=vector_dicts[v.key_overlap], target_path=v.feature_path, target_file_name=v.feature_overlap_save)
	save_dict(target_dict=vector_dicts[v.key_n_verb], target_path=v.feature_path, target_file_name=v.feature_not_verb_save)
	save_dict(target_dict=vector_dicts[v.key_y_verb], target_path=v.feature_path, target_file_name=v.feature_verb_save)
	save_dict(target_dict=vector_dicts[v.key_similar], target_path=v.feature_path, target_file_name=v.feature_similar_save)

	print("\n\tSuccess save files !!\n")


def get_dicts():
	def load_dict(file_path, file_name):
		try:
			with open(file_path + file_name, 'r') as feature_file:
				return json.load(feature_file)
		except IOError:
			print "\n\tCan not find", "'" + file_name + "'", "in the directory ", "'" + file_path + "'", "!!\n"
			sys.exit(1)

	conversation_dict = load_dict(v.dictionary_path, v.conversation_save)
	ontology_dict = load_dict(v.dictionary_path, v.dictionary_save)
	similar_dict = load_dict(v.dictionary_path, v.similar_save)

	vector_dicts = dict()
	vector_dicts[v.key_overlap] = load_dict(v.feature_path, v.feature_overlap_save)
	vector_dicts[v.key_n_verb] = load_dict(v.feature_path, v.feature_not_verb_save)
	vector_dicts[v.key_y_verb] = load_dict(v.feature_path, v.feature_verb_save)
	vector_dicts[v.key_similar] = load_dict(v.feature_path, v.feature_similar_save)

	# print("ontology   dict length :", len(ontology_dict))
	# print("feature overlap length :", len(vector_dicts[v.key_overlap]))
	# print("feature nn verb length :", len(vector_dicts[v.key_n_verb]))
	# print("feature yy verb length :", len(vector_dicts[v.key_y_verb]))
	# print("feature similar length :", len(vector_dicts[v.key_similar]))
	# print("similar    dict length :", len(similar_dict), "\n\n")

	dicts = dict()
	dicts[v.key_conversation] = conversation_dict
	dicts[v.key_ontology] = ontology_dict
	dicts[v.key_similar] = similar_dict
	dicts[v.key_vector] = vector_dicts

	return dicts


def init_similar_dict(ontology_dict):
	similar_dict = dict()

	with open(v.dictionary_path + v.similar_tbl) as similar_file:
		for line in similar_file:
			data = line.strip().split("\t")
			key = data[0]
			try:
				value = data[1].split(",")
			except IndexError:
				continue
			else:
				is_exist = 0
				similar_list = list()

				for keyword in value:
					if keyword in ontology_dict:
						is_exist += 1
						similar_list.append(keyword)

				if is_exist:
					if key not in similar_dict:
						similar_dict[key] = [len(similar_list), similar_list]

	return similar_dict


# key = keyword
# value = [ number of tags, [ tag 1,  tag 2, .... , tag N ], [ count tag 1, count tag 2, .... , count tag N ] ]
def init_ontology_dict(csv_file):
	def _append_max_freq_key(_ontology_dict):
		def _is_verb(_ontology):
			_ontology_list = _ontology.split(TOKEN_VERB)
			if len(_ontology_list) > 1 and _ontology_list[1] == ONTOLOGY_VERB:
				return 1
			elif len(_ontology_list) > 1 and _ontology_list[1] == ONTOLOGY_SUBJECT:
				return -1
			else:
				return 0

		max_freq_verb = 0
		max_freq_not_verb = 0
		max_key_verb = str()
		max_key_not_verb = str()

		for _key in _ontology_dict:
			for _tag_key in _ontology_dict[_key][1]:
				freq = _ontology_dict[_key][1][_tag_key]
				is_verb = _is_verb(_tag_key)
				if is_verb == 1:
					if freq > max_freq_verb:
						max_freq_verb = freq
						max_key_verb = _tag_key
				elif is_verb == -1:
					if freq > max_freq_not_verb:
						max_freq_not_verb = freq
						max_key_not_verb = _tag_key

		_ontology_dict["max_key_verb"] = max_key_verb
		_ontology_dict["max_key_not_verb"] = max_key_not_verb

		return _ontology_dict

	ontology_dict = dict()
	csv_ontology = csv_file[v.columns['ontology']]

	for ontology in csv_ontology:
		if type(ontology) is not float:
			ontology = ontology.split(',')
			for data in ontology:

				data = data.strip().split('/')
				keyword = data[0]
				tag = data[1]

				if keyword not in ontology_dict:
					ontology_dict[keyword] = [0, {}]

				if tag not in ontology_dict[keyword][1]:
					ontology_dict[keyword][0] += 1
					ontology_dict[keyword][1][tag] = 1
				else:
					ontology_dict[keyword][1][tag] += 1

	return _append_max_freq_key(ontology_dict)


# set list of all files from directory
def init_file_dict():
	try:
		file_list = os.listdir(v.speech_file_path)
	except IOError:
		print("\n\tCan't find Speech Files!!\n")
		exit(-1)

	file_dict = dict()

	for file_name in file_list:
		file_name = file_name.split('.')[0]
		names = file_name.split('_')

		key = names[0] + "_" + names[1] + "_" + names[3] + "_" + names[4]
		value = file_name + ".TEXT"
		file_dict[key] = value

	return file_dict


# set vector dict
# key = keyword // value = { tag 1 : { feature 1 : freq, feature 2 : freq, ... , feature N : freq }, ... , tag N }
def init_feature_dicts(csv_file, conversation_dict, ontology_dict, similar_dict):

	def append_feature_dict(_feature_dict, _features):
		if key not in _feature_dict:
			_feature_dict[key] = dict()

		if tag_key not in _feature_dict[key]:
			_feature_dict[key][tag_key] = dict()

		for _feature in _features:
			if _feature in w2v_dict:
				if _feature not in _feature_dict[key][tag_key]:
					_feature_dict[key][tag_key][_feature] = 1
				else:
					_feature_dict[key][tag_key][_feature] += 1

	def append_feature_overlap_dict(_feature_dict, _features):
		if key not in _feature_dict:
			_feature_dict[key] = dict()

		if tag_key not in _feature_dict[key]:
			_feature_dict[key][tag_key] = [1, dict()]
		else:
			_feature_dict[key][tag_key][0] += 1

		for _feature in _features:
			if _feature in w2v_dict:
				if _feature not in _feature_dict[key][tag_key][1]:
					_feature_dict[key][tag_key][1][_feature] = 1
				else:
					_feature_dict[key][tag_key][1][_feature] += 1

	def get_keywords_from_similar_dict(_similar_dict):
		_similar_list = list()

		for _key in _similar_dict:
			for _keyword in _similar_dict[_key][1]:
				if _keyword not in _similar_list:
					_similar_list.append(_keyword)

		return _similar_list

	feature_dicts = dict()
	feature_dicts[v.key_overlap] = dict()
	feature_dicts[v.key_n_verb] = dict()
	feature_dicts[v.key_y_verb] = dict()
	feature_dicts[v.key_similar] = dict()
	similar_list = get_keywords_from_similar_dict(similar_dict)
	csv_ontology = csv_file[v.columns['ontology']]
	position = 0

	for ontology in csv_ontology:
		if type(ontology) is not float:
			ontology = ontology.split(',')
			for data in ontology:
				data = data.strip()
				data = data.split('/')
				key = data[0]
				tag_key = data[1]

				features = get_features(csv_file, conversation_dict, position)

				ontology_list = tag_key.split(TOKEN_VERB)

				# initialize verb feature dict
				if len(ontology_list) > 1 and ontology_list[1] == ONTOLOGY_VERB:
					append_feature_dict(feature_dicts[v.key_y_verb], features)

				# initialize not verb feature dict
				else:
					append_feature_dict(feature_dicts[v.key_n_verb], features)

				# initialize similar feature dict
				if key in similar_list:
					append_feature_dict(feature_dicts[v.key_similar], features)

				# initialize feature dictionary for overlap ontology
				if ontology_dict[key][0] > 1:
					append_feature_overlap_dict(feature_dicts[v.key_overlap], features)

		position += 1

	return feature_dicts


# key = keyword      //  value = { tag 1 : [ vector ],  tag 2 : [ vector ] , ... , tag N : [ vector ] }
def init_vector_dicts(feature_dicts):

	def _init_vector_dict(_feature_dict):
		_vector_dict = dict()
		for _key in _feature_dict:
			_vector_dict[_key] = dict()

			_sum_weight = float()
			for _tag_key in _feature_dict[_key]:
				_sub_feature_dict = _feature_dict[_key][_tag_key]
				for _weight in _sub_feature_dict.values():
					_sum_weight += _weight

			for _tag_key in _feature_dict[_key]:
				_sub_feature_dict = _feature_dict[_key][_tag_key]
				_vector_dict[_key][_tag_key] = get_vector(_sub_feature_dict, _sum_weight)

		return _vector_dict

	def _init_overlap_vector_dict(_feature_dict):
		_vector_dict = dict()
		for _key in _feature_dict:
			_vector_dict[_key] = dict()

			_sum_weight = float()
			for _tag_key in _feature_dict[_key]:
				_sub_feature_dict = _feature_dict[_key][_tag_key][1]
				for _weight in _sub_feature_dict.values():
					_sum_weight += _weight

			for _tag_key in _feature_dict[_key]:
				_tag_key_frequency = _feature_dict[_key][_tag_key][0]
				_sub_feature_dict = _feature_dict[_key][_tag_key][1]
				_vector_dict[_key][_tag_key] = [_tag_key_frequency, get_vector(_sub_feature_dict, _sum_weight)]

		return _vector_dict

	vector_dicts = dict()
	vector_dicts[v.key_overlap] = _init_overlap_vector_dict(feature_dicts[v.key_overlap])
	vector_dicts[v.key_n_verb] = _init_vector_dict(feature_dicts[v.key_n_verb])
	vector_dicts[v.key_y_verb] = _init_vector_dict(feature_dicts[v.key_y_verb])
	vector_dicts[v.key_similar] = _init_vector_dict(feature_dicts[v.key_similar])

	return vector_dicts
