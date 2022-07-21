#!/usr/bin/env/ python

import sys
import itertools
from collections import OrderedDict

#####
# This script takes in two text files: one to be edited, and the second containing tab separated
# to be searched for and replaced in the first file. The output is an edited file with the
# proper changes made.
#####

# check for correct commandline arguments
if len(sys.argv) != 4:
	print("Usage: searchAndReplace.py <file to edit> <file containing edits> <output>")
	sys.exit(0) 

inFile = sys.argv[1]
editFile = sys.argv[2]

# parse changes file into a dictionary
original = []
edited = []
with open(editFile, 'r') as edits:
	for line in edits:
		line = line.strip("\n").split("\t")
		original.append(line[0])
		edited.append(line[1])
editsDict = dict(zip(original, edited))

# read input file
with open(inFile, 'r') as inputFile:
	inputText = inputFile.read() 

# make changes to input data
for org, edit in editsDict.items():
	inputText = inputText.replace(org, edit)

# write output file
with open(sys.argv[3], 'w') as outFile:
	outFile.write(inputText)
