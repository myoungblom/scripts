#!/usr/bin/env python

import sys
import os.path
import itertools
import subprocess

#####
# This script takes in a scoary traits file and uses it to 
# bin isolates into 'target' and 'background' for use with vcflib-wcFst.
# Requirements: vcf file must be correctly formmatted, 
# tabix index file of vcf file must be in cwd (tabix -p vcf <file.vcf.gz)
#####

# check for correct commandline arguments
if len(sys.argv) != 4:
    print("Usage: scoaryToVcflibFst.py <scoaryTraits.csv> <snpvcf.vcf> <headerToParse>")
    sys.exit(0)

scoary = sys.argv[1]
vcfFile = sys.argv[2]
header = str(sys.argv[3])

backgroundList = []
targetList = []
phenotypes = {}
indexes = {}

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

# make dictionary with indices from vcf file
with open(vcfFile, 'r') as vcf:
    for line in vcf:
        line = line.strip("\n")
        if line.startswith("#CHROM"):
            parser = line.split("\t")
            for item in parser[9:]:
                indexes[item] = (parser.index(item))

# read from phenotypes dictionary, write from indexes dictionary into background
# and target lists
for key, value in phenotypes.items():
    if value == "0":
        backgroundList.append(str(indexes[key]-9))
    elif value == "1":
        targetList.append(str(indexes[key]-9))

# join lists to make csv
background = ",".join(backgroundList)
target = ",".join(targetList)

# use background and target lists to run vcflib wcFst
outfile = header+"_wcFst.txt"
with open(outfile, 'w') as output:
    subprocess.call(["/opt/PepPrograms/vcflib/bin/wcFst" ,"--target",target,"--background",\
        background,"--file",vcfFile,"--type", "GT"], stdout=output)
