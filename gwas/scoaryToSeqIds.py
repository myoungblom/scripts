#!/usr/bin/env python

import sys
import itertools

#####
# This script takes in a scoary traits file and parses a  
# given header to write an output file with the ID's
# of isolates positive for that trait.
#####

# check for correct commandline arguments
if len(sys.argv) != 3:
    print("Usage: scoaryToSeqIds.py <scoaryTraits.csv> <headerToParse>")
    sys.exit(0)

scoary = sys.argv[1]
header = str(sys.argv[2])

targetList = []
phenotypes = {}

# make dictionary with binary phenotypes from scoary traits file
with open(scoary, 'r') as scoaryFile:
    for line in scoaryFile:
        line = line.strip("\n")
        line = line.strip("\r")
        parser = line.split(",")
        if line.startswith(","):
            indexed = parser.index(header)
        elif not line.startswith(","):
            value = parser[indexed]
            isolate = parser[0]
            phenotypes[isolate] = value

# read from phenotypes dictionary, write from indices to target list
for key, value in phenotypes.items():
    if value == "1":
        targetList.append(key)

# write target ids to output file
with open(header+"_ids.txt", 'w') as output:
    for i in targetList:
        output.write(i+"\n")
