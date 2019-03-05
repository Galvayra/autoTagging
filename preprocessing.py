#!/usr/bin/python
# -*- coding: utf-8 -*-

from Dataset.set_dictionary import set_dicts
import time
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
start_time = time.time()


if __name__ == '__main__':
	set_dicts()
	print("--- %s seconds ---" % (time.time() - start_time))
