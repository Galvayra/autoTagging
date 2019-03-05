#!/usr/bin/python
# -*- coding: utf-8 -*-
from ontology import Ontology
from Word2Vec.get_vector import get_kkma_features, get_vector, get_arg_max_1_n, is_target_vector_zero
from Word2Vec.read_w2v import w2v_dict
import variables as v
import pandas as pd

ontology = Ontology()


def read_test_csv():
	def _get_target_features(features):
		_target_features = dict()

		for feature in features:
			feature = feature.encode('utf-8')
			if feature in w2v_dict:
				if feature not in _target_features:
					_target_features[feature] = 1
				else:
					_target_features[feature] += 1

		return _target_features

	def _show_answer_dict():

		for k in sorted(answer_dict.keys()):
			accuracy = answer_dict[k]['match'] / float(answer_dict[k]['total'])
			print k
			print "accuracy - ", accuracy
			print answer_dict[k]
			print

	csv_file = pd.read_csv(v.dictionary_path + v.test_manual_csv)
	answer_dict = dict()

	for position, line in enumerate(csv_file[v.columns['ontology']]):

		answer_list = [keyword.strip() for keyword in line.strip().split(",")]

		features = get_kkma_features(csv_file[v.columns['data']][position])
		target_features = _get_target_features(features)
		target_vector = get_vector(target_features, 0)

		for answer in answer_list:

			# initialize or append dictionary of answer
			if answer not in answer_dict:
				answer_dict[answer] = {
					"match": 0,
					"total": 1,
					"zero": 0,
					"unk": 0,
				}
			else:
				answer_dict[answer]["total"] += 1

			keyword = answer.split("/")[0].decode('utf-8')
			tag = answer.split("/")[1].decode('utf-8')

			if is_target_vector_zero(target_vector):
				answer_dict[answer]["zero"] += 1
			else:
				if tag not in ontology.ontology_dict[keyword][1]:
					answer_dict[answer]["unk"] += 1
				else:
					tag_predict = get_arg_max_1_n(ontology.vector_dicts[v.key_overlap][keyword], target_vector)

					if tag == tag_predict:
						answer_dict[answer]["match"] += 1

	_show_answer_dict()

	return answer_dict

if __name__ == '__main__':
	answer_dict = read_test_csv()

	## 여기에 이어서 matplotlib 만들면 될듯

	## answer dict
	## key : 걷다/Others_Predicate,  value : {"total": 총 테스트 개수, "match": 맞춘 개수}

