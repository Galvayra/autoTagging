#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from variables import w2v_file_name, IS_PRE_PROCESSING

try:
    w2v_file = open("KIST/Word2Vec/" + w2v_file_name)
except IOError:
    try:
        w2v_file = open("Word2Vec/" + w2v_file_name)
        is_pre_processing = True
    except IOError:
        print("\n\tCan't find word2vector File !!")
        exit(-1)

dimension = 50

w2v_dict = dict()


def set_w2v_dict(w2v_dict):
    def _get_vector(vector):
        result_vector = list()

        for i in vector:
            result_vector.append(float(i))

        return result_vector

    for line in w2v_file.readlines():
        line = line.split()
        if len(line) is dimension+1:
            key = line[0]
            value = line[1:]

            if IS_PRE_PROCESSING:
                w2v_dict[key.decode('utf-8')] = _get_vector(value)
            else:
                w2v_dict[key] = _get_vector(value)

    return w2v_dict

set_w2v_dict(w2v_dict)
