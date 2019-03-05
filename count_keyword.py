#!/usr/bin/python
# -*- coding: utf-8 -*-

import variables as v
import pandas as pd

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


TOKEN_VERB = '_'
ONTOLOGY_VERB = "Predicate"
ONTOLOGY_SUBJECT = "Subject"
START_UPDATE_POSITION = 30009


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


def print_ontology_dict(_ontology_dict):
	count = 0
	for key in _ontology_dict:
		if type(_ontology_dict[key][0]) == int:
			count += 1

	print "사전 크기 : ", count
	print "====================================================="
	total = 0

	for key in sorted(_ontology_dict.keys()):
		if type(_ontology_dict[key][0]) == int:
			print key.encode('utf-8')
			print _ontology_dict[key]
			for i in _ontology_dict[key][1].values():
				total += i
			print "====================================================="
	print "total keyword frequency - " + str(total)


def print_count_conversation(_csv_file):
	count = 0
	csv_filename = _csv_file[v.columns['name']]
	for line in csv_filename:
		if type(line) is not float:
			count += 1
	print "대화 갯수 : ", count


def print_count_sentence(_csv_file):
	count = 0
	csv_filename = _csv_file[v.columns['keyword']]
	for line in csv_filename:
		if not line.startswith('-'):
			count += 1
	print "문장 갯수 : ", count


def print_test_count_sentence(_csv_file):
	count = 0
	csv_keyword = _csv_file[v.columns['keyword']]
	csv_ontology = _csv_file[v.columns['ontology']]
	for position, line in enumerate(csv_keyword):
		if not line.startswith('-'):
			if type(csv_ontology[position]) is not str:
				count += 1

	print "문장 갯수 : ", count


def print_count_overlap(_ontology_dict):
	count = 0
	total = 0
	print "====================================================="
	for key in sorted(_ontology_dict.keys()):
		if len(_ontology_dict[key][1])>=2:
			print key.encode('utf-8')
			print _ontology_dict[key]
			for i in _ontology_dict[key][1].values():
				total += i
			print "====================================================="
	print "total keyword frequency - " + str(total)

#
# def counting_search_keyword(_csv_file):
# 	csv_keyword = _csv_file[v.columns['keyword']][START_UPDATE_POSITION:]
#
# 	for position, raw_data in enumerate(csv_keyword):
# 		if raw_data is not "-":


if __name__ == '__main__':
	csv_file = pd.read_csv(v.dictionary_path + "auto_" + v.target_csv)
	print_test_count_sentence(csv_file)
