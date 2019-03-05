#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Word2Vec.get_vector4corpus import get_kkma_features
import getopt
import sys
options, args = getopt.getopt(sys.argv[1:], 'f:')


def list2sent(features, _cut_freq):
	string = str()
	count = 0

	for feature in features:
		string += feature+' '
		count += 1

	if count > _cut_freq:
		return string, True
	else:
		return string, False


def write_file(files, _cut_freq):
	output = len(files)-1

	with open(files[output], 'w') as w_file:
		for file in files[:output]:
			print("\n\nReading", file)
			with open(file, 'r') as read_file:
				lines = read_file.readlines()
				count = 0
				length = len(lines)
				for line in lines:
					show_progress(count, length)
					newline, has_morpheme = list2sent(get_kkma_features(line), _cut_freq)

					if has_morpheme:
						w_file.write(newline.strip()+"\n")

					count += 1


# show making vector progress
def show_progress(_count, _sent_count):
	print(_count, _sent_count/10)
	if _count % int(_sent_count/10) == 0:
		progress = " >>"
		progress_count = int((_count / _sent_count) * 10)
		progress = progress_count * progress
		progress += (10 - progress_count) * "   "
		print("[%s ] %4d%%" % (progress, progress_count * 10))

if __name__ == '__main__':

	if len(options) == 0:
		cut_freq = 0
	else:
		cut_freq = int(options[0][1])

	write_file(args, cut_freq)
