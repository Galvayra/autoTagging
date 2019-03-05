#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import sys
import operator

reload(sys)
sys.setdefaultencoding('utf-8')


TOKEN_VERB = '_'
ONTOLOGY_VERB = "Predicate"
ONTOLOGY_SUBJECT = "Subject"

DICTIONARY_PATH = 'Dataset/'
# DICTIONARY_CSV = 'final_manual.csv'
DICTIONARY_CSV = 'auto_final_target.csv'


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
	csv_ontology = csv_file['Ontology']

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
			local_total = 0
			for i in _ontology_dict[key][1].values():
				local_total += i
			total += local_total

			print key.encode('utf-8'), ":",  local_total
			print [_ontology_dict[key][0], _ontology_dict[key][1]]
			print "====================================================="
	print "total - " + str(total)


def print_1_1_dict(_ontology_dict):
	count = 0
	for key in _ontology_dict:
		if type(_ontology_dict[key][0]) == int and _ontology_dict[key][0] == 1:

			tag_key = _ontology_dict[key][1].keys()

			is_verb = tag_key[0].split("/")
			#
			# if is_verb[0].endswith("Predicate"):
			# 	count += 1

			count += 1

	print "사전 크기 : ", count
	print "====================================================="
	total = 0

	for key in sorted(_ontology_dict.keys()):
		if type(_ontology_dict[key][0]) == int and _ontology_dict[key][0] == 1:

			# tag_key = _ontology_dict[key][1].keys()
			#
			# is_verb = tag_key[0].split("/")
			#
			# if is_verb[0].endswith("Predicate"):
			# 	local_total = 0
			# 	for i in _ontology_dict[key][1].values():
			# 		local_total += i
			# 	total += local_total
			#
			# 	print key.encode('utf-8'), ":", local_total
			# 	print [_ontology_dict[key][0], _ontology_dict[key][1]]
			#
			# 	print "====================================================="

			local_total = 0
			for i in _ontology_dict[key][1].values():
				local_total += i
			total += local_total

			print key.encode('utf-8'), ":", local_total
			print [_ontology_dict[key][0], _ontology_dict[key][1]]

			print "====================================================="
	print "total - ", total


def print_overlap_dict(_ontology_dict):
	count = 0
	for key in _ontology_dict:
		if type(_ontology_dict[key][0]) == int and _ontology_dict[key][0] > 1:
			count += 1

	total = 0
	print "사전 크기 : ", count
	print "====================================================="
	for key in sorted(_ontology_dict.keys()):
		if type(_ontology_dict[key][0]) == int and _ontology_dict[key][0] > 1:
			local_total = 0
			for i in _ontology_dict[key][1].values():
				local_total += i
			total += local_total

			print key.encode('utf-8'), ":",  local_total
			print [_ontology_dict[key][0], _ontology_dict[key][1]]
			print "====================================================="
	print "total - ",


def print_keys(_ontology_dict):
	key_dict = dict()
	for key in _ontology_dict:
		if type(_ontology_dict[key][0]) == int:
			sub_dict = _ontology_dict[key][1]

			for sub_key in sub_dict:
				if sub_key not in key_dict:
					key_dict[sub_key] = int(sub_dict[sub_key])
				else:
					key_dict[sub_key] += int(sub_dict[sub_key])

	sorted_x = sorted(key_dict.items(), key=operator.itemgetter(1), reverse=True)

	for key in sorted_x:
		print key[0].ljust(20), str(key[1]).rjust(5)

if __name__ == '__main__':

	csv_file = pd.read_csv(DICTIONARY_PATH + DICTIONARY_CSV)
	ontology_dict = init_ontology_dict(csv_file)

	try:
		if sys.argv[1] == "--all":
			print_ontology_dict(ontology_dict)
		if sys.argv[1] == "--one":
			print_1_1_dict(ontology_dict)
		elif sys.argv[1] == "--overlap":
			print_overlap_dict(ontology_dict)
	except IndexError:
		print_keys(ontology_dict)

