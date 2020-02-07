#!/usr/bin/env python

import sys
import itertools

#####
# This script takes in a scoary traits file and outputs a text file
# with the vcf indexes of isolates positive or negative for a given trait
# in 2 files: target and background. This script is meant for use with
# vcflib to calculate Fst values from a snp-vcf file.
#####

# check for correct commandline arguments
if len(sys.argv) != 4:
    print("Usage: vcflibInput.py <scoaryInput.csv> <snpvcf.vcf> <headerToParse>")
    sys.exit(0)


scoary = sys.argv[1]
vcfFile = sys.argv[2]
header = str(sys.argv[3])
outBackground = header+"_background.csv"
outB = open(outBackground, 'w')
outTarget = header+"_target.csv"
outT = open(outTarget, 'w')

background = []
target = []
phenotypes = {}
indexes = {}

# make dictionary with binary phenotypes from scoary traits file
with open(scoary, 'r') as scoaryFile:
    for line in scoaryFile:
        line = line.strip("\n")
        parser = line.split(",")
        if line.startswith(","):
            indexed = parser.index(header)
        elif not line.startswith(","):
            value = parser[indexed]
            isolate = parser[0]
            phenotypes[isolate] = value

# make dictionary with indices from vcf file
with open(vcfFile, 'r') as vcf:
    for line in vcf:
        line = line.strip("\n")
        if line.startswith("#CHROM"):
            parser = line.split("\t")
            for item in parser[9:]:
                indexes[item] = parser.index(item)

# read from phenotypes dictionary, write from indexes dictionary into background
# and target lists
for key, value in phenotypes.iteritems():
    if value == "0":
        background.append(str(indexes[key]))
    elif value == "1":
        target.append(str(indexes[key]))

# join lists to make csv
backgroundID = ",".join(background)
targetID = ",".join(target)

# write csv lists to outfiles
outB.write(backgroundID)
outT.write(targetID)
outB.close()
outT.close()
