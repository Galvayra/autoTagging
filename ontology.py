#!/usr/bin/python
# -*- coding: utf-8 -*-

from Dataset.set_dictionary import get_dicts
from Word2Vec.get_vector import *
from Word2Vec.read_w2v import w2v_dict
import variables as v
import pandas as pd
import sys
import Word2Vec.read_w2v as w2v

reload(sys)
sys.setdefaultencoding('utf-8')


KEY_TAG = "Tag"
KEY_KEYWORD = "Keyword"
MAX_KEY_VERB = "max_key_verb"
MAX_KEY_NOT_VERB = "max_key_not_verb"
TEST_SAMPLE_RATIO = 10

# set position to start for updating row number
START_UPDATE_POSITION = 30009


class Ontology:
	columns = {'text': 'TEXT', 'keyword': 'KEYWORD'}

	def __init__(self):
		dicts = get_dicts()
		self.conversation_dict = dicts[v.key_conversation]
		self.ontology_dict = dicts[v.key_ontology]
		self.similar_dict = dicts[v.key_similar]
		self.vector_dicts = dicts[v.key_vector]

	def automatic_filling(self, do_test=False):

		def _get_raw_data(_raw_data):
			_raw_data = _raw_data.strip()
			if _raw_data.endswith(','):
				_raw_data = _raw_data[:-1]

			return _raw_data

		def _set_write_data(_ontology_list):
			_write_data = list()

			# copy original ontology to update csv file
			for i in range(START_UPDATE_POSITION):
				tagging_string = _ontology_list[i]

				if type(tagging_string) == str:
					_write_data.append(tagging_string)
				else:
					_write_data.append(str())

			# copy new ontology automatically tagged to update csv file
			for _position in range(START_UPDATE_POSITION, len(_ontology_list)):
				tagging_string = str()

				if _position in tagging_dict:
					length = len(tagging_dict[_position]) - 1
					for i in range(0, length):
						tagging_string += tagging_dict[_position][i] + ", "
					tagging_string += tagging_dict[_position][length]
				_write_data.append(tagging_string)

			return _write_data

		def _set_testing_dict():
			_testing_dict = dict()

			with open(v.dictionary_path + v.overlap_keyword_file) as w_file:
				for _line in w_file:
					# [ count, [ position list ] ]
					_testing_dict[_line.strip().decode('utf-8')] = {
						"count": 0,
						"pos": list(),
						"test": list()
					}

			# PASS 1 : set position of all of sentences in the keyword of 1:N target
			for _position, _raw_data in enumerate(csv_keyword):
				if _raw_data is not "-":
					_raw_data = _get_raw_data(_raw_data)

					_keyword_dict = dict()

					for _keyword in _raw_data.split(','):
						_keyword = _keyword.strip()
						_keyword = _keyword.decode('utf-8')

						if _keyword not in _keyword_dict:
							_keyword_dict[_keyword] = 1
						else:
							_keyword_dict[_keyword] += 1

					for _keyword in _keyword_dict:

						# dictionary has target key
						if _keyword in self.ontology_dict:

							# 1:N keyword in target test
							if _keyword in _testing_dict and _keyword_dict[_keyword] is 1:
								_testing_dict[_keyword]["pos"].append(_position)

			# PASS 2 : set position of testing sentences
			for _position, _raw_data in enumerate(csv_keyword):
				if _raw_data is not "-":
					_raw_data = _get_raw_data(_raw_data)
					_keyword_1_n_list = list()

					for _keyword in _raw_data.split(','):
						_keyword = _keyword.strip()
						_keyword = _keyword.decode('utf-8')

						if _keyword in _testing_dict:
							_keyword_1_n_list.append(_keyword)

					if _keyword_1_n_list:

						for _keyword in _keyword_1_n_list:

							# if is target
							if _position in _testing_dict[_keyword]["pos"]:
								_testing_dict[_keyword]["count"] += 1

								if _testing_dict[_keyword]["count"] % TEST_SAMPLE_RATIO == 0:
									_testing_dict[_keyword]["test"].append(_position)

			# _position_list = list()
			# _count = 0
			# for _test_keyword in _testing_dict:
			# 	for _position in _testing_dict[_test_keyword]["test"]:
			# 		_count += 1
			# 		if _position not in _position_list:
			# 			_position_list.append(_position)
			# 		else:
			# 			print "overlap sentence in the target csv file -", _position + START_UPDATE_POSITION + 2
			#
			# print "# of total sentence except for overlapping -", len(_position_list)
			# print "# of total sentence -", _count

			return _testing_dict

		csv_file = pd.read_csv(v.dictionary_path + v.target_csv)

		csv_keyword = csv_file[v.columns['keyword']][START_UPDATE_POSITION:]

		tagging_dict = dict()

		if do_test:
			testing_dict = _set_testing_dict()
			test_pos_list = list()
			for i, va in testing_dict.items():
				print i, len(va["test"])
				print va["test"]
			#
			# 	for pos in va["test"]:
			# 		pos = pos + START_UPDATE_POSITION + 2
			# 		if pos not in test_pos_list:
			# 			test_pos_list.append(pos)
			#
			# test_pos_list = sorted(test_pos_list)
			# print
			# print test_pos_list

		count_all = 0
		count_1_1 = 0
		count_1_N = 0
		count_1_N_ = 0
		count_1_N_vector_zero_verb = 0
		count_1_N_vector_zero_noun = 0
		count_1_N_test = 0
		count_similar = 0
		count_similar_not = 0
		count_similar_1_1 = 0
		count_similar_1_N = 0
		count_similar_1_N_ = 0
		count_similar_M_N = 0
		count_similar_M_N_ = 0
		count_similar_1_N_vector_zero_verb = 0
		count_similar_M_N_vector_zero_verb = 0
		count_similar_1_N_vector_zero_noun = 0
		count_similar_M_N_vector_zero_noun = 0
		count_not_exist = 0
		count_not_exist_verb = 0
		count_not_exist_noun = 0
		count_not_exist_vector_zero_verb = 0
		count_not_exist_vector_zero_noun = 0

		for position, raw_data in enumerate(csv_keyword):
			if raw_data is not "-":
				raw_data = _get_raw_data(raw_data)

				# except test sentence
				if do_test:
					is_test_sentence = False

					for test_keyword in testing_dict:
						if position in testing_dict[test_keyword]["test"]:
							is_test_sentence = True

					if is_test_sentence:
						continue

				sentence = csv_file[v.columns['data']][position + START_UPDATE_POSITION]
				agent_sentence = get_agent_sentence(csv_file, self.conversation_dict, position + START_UPDATE_POSITION)

				target_features = dict()
				target_features = self.set_target_features(target_features, sentence)

				if agent_sentence:
					target_features = self.set_target_features(target_features, agent_sentence)

				target_vector = get_vector(target_features, 0)
				keyword_list = list()

				for keyword in raw_data.split(','):
					keyword = keyword.strip()
					keyword = keyword.decode('utf-8')
					count_all += 1
					tag = str()

					# dictionary has target key
					if keyword in self.ontology_dict:
						tag_keys = self.ontology_dict[keyword][1].keys()

						# 1:1 mapping
						if self.ontology_dict[keyword][0] == 1:
							count_1_1 += 1
							for tag in tag_keys:
								tag = tag
						# 1:N mapping
						else:
							count_1_N += 1
							if is_target_vector_zero(target_vector):
								if is_kkma_verb(keyword):
									tag = self.ontology_dict[MAX_KEY_VERB]
									count_1_N_vector_zero_verb += 1
								else:
									tag = self.ontology_dict[MAX_KEY_NOT_VERB]
									count_1_N_vector_zero_noun += 1
							else:
								count_1_N_ += 1
								tag = get_arg_max_1_n(self.vector_dicts[v.key_overlap][keyword], target_vector)

					# dictionary doesn't have target key
					else:
						count_not_exist += 1
						# if similar dictionary has a key
						if keyword in self.similar_dict:
							count_similar += 1
							key_list = self.similar_dict[keyword][1]
							count_of_words = self.similar_dict[keyword][0]

							# the count of similar words is 1
							if count_of_words == 1:
								key = key_list[0]
								tag_keys = self.ontology_dict[key][1].keys()

								# 1:1 mapping
								if self.ontology_dict[key][0] == 1:
									count_similar_1_1 += 1
									for tag in tag_keys:
										tag = tag
								# 1:N mapping
								else:
									count_similar_1_N += 1
									if is_target_vector_zero(target_vector):
										if is_kkma_verb(keyword):
											count_similar_1_N_vector_zero_verb += 1
											tag = self.ontology_dict[MAX_KEY_VERB]
										else:
											count_similar_1_N_vector_zero_noun += 1
											tag = self.ontology_dict[MAX_KEY_NOT_VERB]
									else:
										count_similar_1_N_ += 1
										tag = get_arg_max_1_n(self.vector_dicts[v.key_overlap][key], target_vector)

							# the count of similar words is more than 1
							else:
								count_similar_M_N += 1
								similar_vector_dict = self.init_similar_vector_dict(key_list, self.vector_dicts[v.key_similar])
								if is_target_vector_zero(target_vector):
									if is_kkma_verb(keyword):
										count_similar_M_N_vector_zero_verb += 1
										tag = self.ontology_dict[MAX_KEY_VERB]
									else:
										count_similar_M_N_vector_zero_noun += 1
										tag = self.ontology_dict[MAX_KEY_NOT_VERB]
								else:
									count_similar_M_N_ += 1
									tag, key_max = get_arg_max_from_all_dict(similar_vector_dict, target_vector)

						# if similar dictionary has not a key
						else:
							count_similar_not += 1
							if is_target_vector_zero(target_vector):
								if is_kkma_verb(keyword):
									count_not_exist_vector_zero_verb += 1
									tag = self.ontology_dict[MAX_KEY_VERB]
								else:
									count_not_exist_vector_zero_noun += 1
									tag = self.ontology_dict[MAX_KEY_NOT_VERB]
							else:
								if is_kkma_verb(keyword):
									count_not_exist_verb += 1
									tag, key_max = get_arg_max_from_all_dict(self.vector_dicts[v.key_y_verb], target_vector)
								else:
									count_not_exist_noun += 1
									tag, key_max = get_arg_max_from_all_dict(self.vector_dicts[v.key_n_verb], target_vector)

					# print "\n\t핵심어 : ", keyword.ljust(20), "Tag : ", tag
					keyword_list.append(keyword + "/" + tag)

				tagging_dict[position + START_UPDATE_POSITION] = keyword_list

		print "\n\nAll Counts						: ", count_all
		print "- 1:1 mapping case				: ", count_1_1
		print "- 1:N mapping case				: ", count_1_N
		if do_test:
			print "- 1:N test case					: ", count_1_N_test
		print "  - 1:N mapping					: ", count_1_N_
		print "  - 1:N mapping zero verb		: ", count_1_N_vector_zero_verb
		print "  - 1:N mapping zero noun		: ", count_1_N_vector_zero_noun
		print "- Not Exist case				: ", count_not_exist
		print "  - similar case				: ", count_similar
		print "    - 1:1 similar case			: ", count_similar_1_1
		print "    - 1:N similar case			: ", count_similar_1_N
		print "      - 1:N similar 			: ", count_similar_1_N_
		print "      - 1:N similar zero verb	: ", count_similar_1_N_vector_zero_verb
		print "      - 1:N similar zero noun	: ", count_similar_1_N_vector_zero_noun
		print "    - M:N similar case			: ", count_similar_M_N
		print "      - M:N similar 			: ", count_similar_M_N_
		print "      - M:N similar zero verb	: ", count_similar_M_N_vector_zero_verb
		print "      - M:N similar zero noun	: ", count_similar_M_N_vector_zero_noun
		print "  - Not similar case			: ", count_similar_not
		print "    - Not Exist verb			: ", count_not_exist_verb
		print "    - Not Exist noun			: ", count_not_exist_noun
		print "    - Not Exist zero verb		: ", count_not_exist_vector_zero_verb
		print "    - Not Exist zero noun		: ", count_not_exist_vector_zero_noun

		csv_file[v.columns['ontology']] = _set_write_data(csv_file[v.columns['ontology']])

		df = pd.DataFrame(csv_file, columns=v.columns.values())
		df.to_csv(v.dictionary_path + "auto_" + v.target_csv, index=False)

		if do_test:
			print "\n\n", "keyword".ljust(10), "total count".rjust(10), "test count".rjust(10)
			csv_file_test = dict()

			# erase all of data in csv_file
			for col_key in v.columns.values():
				csv_file_test[col_key] = list()

			for test_keyword in testing_dict:
				print test_keyword, "\t\t", str(testing_dict[test_keyword]["count"]).rjust(10), str(len(testing_dict[test_keyword]["test"])).rjust(10)

				# copy rows
				for position in testing_dict[test_keyword]["test"]:
					# copy columns
					for _col_key in v.columns.values():
						csv_file_test[_col_key].append(csv_file[_col_key][position + START_UPDATE_POSITION])

			df = pd.DataFrame(csv_file_test, columns=v.columns.values())
			df.to_csv(v.dictionary_path + v.test_csv, index=False)

	# return tags which are automatically decided by system
	def semantic_tagging(self, json_input):

		def _get_values(_value):
			if type(_value) == list or type(_value) == unicode:
				return _value
			elif type(_value) == dict:
				return _value["value"]

		try:
			keywords = _get_values(json_input[self.columns['keyword']])
			sentence = _get_values(json_input[self.columns['text']])
		except TypeError:
			return False

		target_features = dict()
		target_features = self.set_target_features(target_features, sentence)
		target_vector = get_vector(target_features, 0)
		tags = list()

		for key in keywords:
			tag_dict = dict()
			tag = str()

			# dictionary has target key
			if key in self.ontology_dict:
				tag_keys = self.ontology_dict[key][1].keys()

				# 1:1 mapping
				if self.ontology_dict[key][0] == 1:
					for tag in tag_keys:
						tag = tag
				# 1:N mapping
				else:
					print "\n1:N mapping "
					tag = get_arg_max_1_n(self.vector_dicts[v.key_overlap][key], target_vector)
					print "Keyword : ", key, "\t\tOntology : ", tag

			# dictionary doesn't have target key
			else:
				# if similar dictionary has a key
				if key in self.similar_dict:
					key_list = self.similar_dict[key][1]
					count_of_words = self.similar_dict[key][0]

					# the count of similar words is 1
					if count_of_words == 1:
						similar_key = key_list[0]
						tag_keys = self.ontology_dict[similar_key][1].keys()

						# 1:1 mapping
						if self.ontology_dict[similar_key][0] == 1:
							for tag in tag_keys:
								tag = tag

							print "\nNot Exist - similar dict 1:1 "
							print "Keyword : ", key, "\t\tOntology : ", tag
						# 1:N mapping
						else:
							if is_target_vector_zero(target_vector):
								if is_kkma_verb(key):
									tag = self.ontology_dict[MAX_KEY_VERB]
								else:
									tag = self.ontology_dict[MAX_KEY_NOT_VERB]
							else:
								print "\nNot Exist - similar dict 1:N "
								tag = get_arg_max_1_n(self.vector_dicts[v.key_overlap][similar_key], target_vector)
								print "Keyword : ", key, "\t\tOntology : ", tag, "\t\tSimilar Keyword : ", similar_key

					# the count of similar words is more than 1
					else:
						similar_vector_dict = self.init_similar_vector_dict(key_list, self.vector_dicts[v.key_similar])
						if is_target_vector_zero(target_vector):
							if is_kkma_verb(key):
								tag = self.ontology_dict[MAX_KEY_VERB]
								key_max = "target is zero (verb)"
							else:
								tag = self.ontology_dict[MAX_KEY_NOT_VERB]
								key_max = "target is zero (noun)"
						else:
							print "\nNot Exist - similar dict N:M "
							tag, key_max = get_arg_max_from_all_dict(similar_vector_dict, target_vector)
							print "Keyword : ", key, "\t\tOntology : ", tag,  "\t\t유사어 : ", key_max

				else:
					print "\nNot Exist"
					if is_kkma_verb(key):
						vv = "\t\tverb"
						if is_target_vector_zero(target_vector):
							tag = self.ontology_dict[MAX_KEY_VERB]
							key_max = "target is zero (verb)"
						else:
							tag, key_max = get_arg_max_from_all_dict(self.vector_dicts[v.key_y_verb], target_vector)
					else:
						if is_target_vector_zero(target_vector):
							tag = self.ontology_dict[MAX_KEY_NOT_VERB]
							key_max = "target is zero (noun)"
						else:
							tag, key_max = get_arg_max_from_all_dict(self.vector_dicts[v.key_n_verb], target_vector)

					print "Keyword : ", key, "\t\tOntology : ", tag,  "\t\t유사어 : ", key_max

			tag_dict[KEY_TAG] = tag
			tag_dict[KEY_KEYWORD] = key
			tags.append(tag_dict)

		json_input['CONTEXT'] = tags

		return json_input

	def set_target_features(self, target_features, sentence):
		for feature in get_kkma_features(sentence):
			feature = feature.encode('utf-8')
			if feature in w2v_dict:
				if feature not in target_features:
					target_features[feature] = 1
				else:
					target_features[feature] += 1

		return target_features

	def init_similar_vector_dict(self, key_list, vector_dict):
		similar_vector_dict = dict()

		for key in key_list:
			similar_vector_dict[key] = vector_dict[key]

		return similar_vector_dict
