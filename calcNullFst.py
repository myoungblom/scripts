#!/usr/bin/env python

import sys
import numpy as np
import subprocess

#####
# This script permutes Fst calculations for creating a null distribution
# which is used to identify Fst outliers. Requires vcflib compatible snp vcf file.
#####

# check for correct arguments
if len(sys.argv) != 4:
    print("Usage: calcNullFst.py <vcflib.vcf> <total isolates> <target #>")
    sys.exit(0)


vcf = sys.argv[1]
total = int(sys.argv[2])
targetNum = int(sys.argv[3])

# make list of isolate vcf indices
isolate = []
for i in range(total):
    isolate.append(i)

# run 100 Fst calculations based on target size
for i in range(100):
    output = open(str(i)+"_wcFst.txt", 'w')
    target = list(np.random.choice(isolate, size=targetNum, replace=False))
    background = []
    for iso in isolate:
        if iso not in target:
           background.append(iso)
    targetArg = ",".join(str(x) for x in list(target))
    backgroundArg = ",".join(str(x) for x in list(background))
    subprocess.call(["/opt/PepPrograms/vcflib/bin/wcFst","--target",targetArg,"--background",\
            backgroundArg, "--file", vcf, "--type", "GT"], stdout=output)
    output.close()

# find maximum wcFst value in null distribution
allFst = []
for i in range(100):
    with open(str(i)+"_wcFst.txt", "r") as f:
        for line in f:
            line = line.strip("\n")
            info = line.split("\t")
            allFst.append(info[4])

maxFst = max(allFst)
print("Max null value: "+maxFst)
