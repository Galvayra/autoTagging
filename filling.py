#!/usr/bin/python
# -*- coding: utf-8 -*-

from ontology import Ontology
import time

start_time = time.time()


if __name__ == '__main__':
	myOntology = Ontology()
	myOntology.automatic_filling(do_test=True)
	print("--- %s seconds ---" % (time.time() - start_time))
