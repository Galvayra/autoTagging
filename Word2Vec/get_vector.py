#!/usr/bin/python
# -*- coding: utf-8 -*-

from Word2Vec.read_w2v import w2v_dict, dimension
from konlpy.tag import Kkma
import json
import variables as v
import numpy as np
import math

kkma = Kkma()


# a set of feature after analyzing sentence using Kkma morpheme
def get_kkma_features(sentence):
    string = str()
    features = list()

    for word in kkma.pos(sentence):
        if word[1].startswith('NN') or word[1].startswith('VV') or word[1].startswith('VA'):
            features.append(word[0]+"/"+word[1])
            string += word[0]+"/"+word[1]+" "

    return features


# a set of feature after analyzing sentence using Kkma morpheme
def is_kkma_verb(keyword):
    string = str()
    features = list()
    is_verb = False

    keyword = keyword.split('(')[0]

    for word in kkma.pos(keyword):
        if word[1].startswith('NN'):
            features.append(word[0]+"/"+word[1])
            string += word[0]+"/"+word[1]+" "

        elif word[1].startswith('VV') or word[1].startswith('VA'):
            features.append(word[0]+"/"+word[1])
            string += word[0]+"/"+word[1]+" "
            is_verb = True

    return is_verb


# get features from target sentence and agent sentence and then using morpheme analyzer
def get_agent_sentence(csv_file, conversation_dict, position):
    csv_name = csv_file[v.columns["name"]]
    csv_start = csv_file[v.columns["start"]]

    # get features from agent sentence
    def _get_agent_sentence(file_name, _start_position):
        with open(v.speech_file_path + file_name, 'r') as target_file:
            target_file = json.load(target_file)

            target_text = target_file["TEXT"]
            _position = 0

            for sentence in target_text:
                target = str(sentence["start"])
                if target == _start_position:
                    break
                _position += 1

            # Can not search start position in the target file
            if len(target_text) == _position:
                return list()

            # search agent sentence form target file
            while target_text[_position]['user_type'] == 'user':
                _position -= 1

                # There is no target_text
                if _position < 0:
                    return list()

            agent_sentence = target_text[_position]['text']

            return agent_sentence

    start_position = csv_start[position]
    position = position

    # search file name from csv file
    while type(csv_name[position]) is float:
        position -= 1

    key = csv_name[position]

    # Conversation is existed
    if key in conversation_dict:
        return _get_agent_sentence(conversation_dict[key], str(start_position))

    # Conversation isn't existed
    else:
        return str()


# get features from target sentence and agent sentence and then using morpheme analyzer
def get_features(csv_file, conversation_dict, position):
    csv_name = csv_file[v.columns["name"]]
    csv_start = csv_file[v.columns["start"]]
    target_sentence = csv_file[v.columns['data']][position]
    features = list()

    # get features from agent sentence
    def _get_agent_sentence(file_name, _start_position):
        with open(v.speech_file_path + file_name, 'r') as target_file:
            target_file = json.load(target_file)

            target_text = target_file["TEXT"]
            _position = 0

            for sentence in target_text:
                target = str(sentence["start"])
                if target == _start_position:
                    break
                _position += 1

            # Can not search start position in the target file
            if len(target_text) == _position:
                return list()

            # search agent sentence form target file
            while target_text[_position]['user_type'] == 'user':
                _position -= 1

                # There is no target_text
                if _position < 0:
                    return list()

            agent_sentence = target_text[_position]['text']

            return get_kkma_features(agent_sentence)

    start_position = csv_start[position]
    position = position

    # search file name from csv file
    while type(csv_name[position]) is float:
        position -= 1

    key = csv_name[position]

    # Conversation is existed
    if key in conversation_dict:
        features = get_kkma_features(target_sentence) + _get_agent_sentence(conversation_dict[key], str(start_position))

    # Conversation isn't existed
    else:
        features = get_kkma_features(target_sentence)

    return features
    # # except overlapping items
    # return set(features)


# key = keyword      //  value = { tag 1 : [ vector ],  tag 2 : [ vector ] , ... , tag N : [ vector ] }
def init_vector_dicts(feature_dicts):

    def init_vector_dict(feature_dict):
        vector_dict = dict()
        for key in feature_dict:
            vector_dict[key] = dict()
            for tag_key in feature_dict[key]:
                features = feature_dict[key][tag_key]
                vector_dict[key][tag_key] = get_vector(features)

        return vector_dict

    vector_dicts = dict()
    vector_dicts[v.key_overlap] = init_vector_dict(feature_dicts[v.key_overlap])
    vector_dicts[v.key_n_verb] = init_vector_dict(feature_dicts[v.key_n_verb])
    vector_dicts[v.key_y_verb] = init_vector_dict(feature_dicts[v.key_y_verb])
    vector_dicts[v.key_similar] = init_vector_dict(feature_dicts[v.key_similar])

    return vector_dicts


# get centroid vector from the features
def get_vector(feature_dict, sum_weight):

    def sum_vector(_vector, _target_vector, _target_weight):
        _result_vector = list()
        for index in range(dimension):
            _result_vector.append(_vector[index] + (_target_vector[index] * _target_weight))

        return _result_vector

    def div_vector(_vector, _count):
        _result_vector = list()
        for index in range(dimension):
            _result_vector.append(_vector[index] / _count)

        return _result_vector
        # if _count == 0:
        #     return _vector
        # else:
        #     _result_vector = list()
        #     for index in range(dimension):
        #         _result_vector.append(_vector[index] / _count)
        #
        #     return _result_vector

    def get_sum_weight(_feature_dict):
        _sum_weight = float()

        for _feature in _feature_dict:
            _sum_weight += _feature_dict[_feature]

        return _sum_weight

    def get_target_weight(_target_weight, _sum_weight):
        _result_weight = -math.log10(float(_target_weight) / _sum_weight)

        # If the total counts of features (_sum_weight) is same to each of features count (_target_weight)
        if _result_weight:
            return 1 / _result_weight
        else:
            return 1.0

    result_vector = list()
    for i in range(dimension):
        result_vector.append(0.0)

    if len(feature_dict):
        count = 0

        # sum_weight != 0  >>  preprocessing sentence
        # sum_weight == 0  >>  automatic tagging sentence
        if sum_weight == 0:
            sum_weight = get_sum_weight(feature_dict)

        # sum of the vectors
        for feature in feature_dict.keys():
            count += 1
            target_weight = get_target_weight(feature_dict[feature], sum_weight)
            result_vector = sum_vector(result_vector, w2v_dict[feature], target_weight)
            # if feature in w2v_dict:
            #     count += 1
            #     target_weight = get_target_weight(feature_dict[feature], sum_weight)
            #     result_vector = sum_vector(result_vector, w2v_dict[feature], target_weight)

        return div_vector(result_vector, count)

    # there are no co-occur keywords in the sentences
    else:
        return result_vector


# if target is none
def is_target_vector_zero(target_vector):
    if np.count_nonzero(target_vector):
        return False
    else:
        return True


def get_arg_max_1_n(vector_dict, target_vector):
    arg_max = str()
    sim_max = 0
    _dict = dict()

    target_vector = np.reshape(target_vector, (50, 1))

    for tag_key in vector_dict:
        similarity = np.dot(vector_dict[tag_key][1], target_vector)
        _dict[float(similarity)] = tag_key
        if sim_max < similarity:
            sim_max = similarity
            arg_max = tag_key
	#
    # for key in sorted(_dict, reverse=True):
    #     print _dict[key].ljust(30), key

    return arg_max


def get_arg_max_from_all_dict(vector_dict, target_vector):
    arg_max = str()
    sim_max = 0
    key_max = str()

    target_vector = np.reshape(target_vector, (50, 1))

    for key in vector_dict:
        for tag_key in vector_dict[key]:
            similarity = np.dot(vector_dict[key][tag_key], target_vector)

            if sim_max < similarity:
                sim_max = similarity
                arg_max = tag_key
                key_max = key

    return arg_max, key_max
