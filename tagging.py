#!/usr/bin/python
# -*- coding: utf-8 -*-
from ontology import Ontology
import json


if __name__ == '__main__':
	ontology = Ontology()

	while True:
		string_input = raw_input("\n\n\n입력 (EXIT) = ")

		if string_input == "EXIT":
			break

		try:
			json_input = json.loads(string_input)
		except ValueError:
			print "\n\n\nNot Valid JSON Format - ", string_input
		else:
			print "Sentence -", string_input

			json_output = ontology.semantic_tagging(json_input)

			if json_output:
				pass
			else:
				print "\n\n\nNot Valid JSON Format - ", string_input
