#!/usr/bin/env python3

import sys
import shutil
import subprocess
import os
import pandas as pd

#####
# This script takes a snp-sites vcf and converts it to a 
# snp matrix to be used with treeWAS.
#####

# check for correct arguments
if len(sys.argv) != 2:
    print("Usage: snpVcfToTreeWAS.py <snpsites.vcf>")
    sys.exit(0)

vcf = sys.argv[1]
outfile = ".".join(vcf.split(".")[:-1])+"_treewasSNPs.txt"

# copy snpvcf to temp file
temp = ".".join(vcf.split(".")[:-1])+".tmp"
shutil.copyfile(vcf, temp)

# remove ambiguous and non-biallelic sites
subprocess.call(["sed", "-i", "/\*/d", temp])
subprocess.call(["sed", "-i","/\,/d", temp])

# reformat vcf for treeWAS
temp2file = temp.strip(".tmp")+".tmp2"
temp2 = open(temp2file, "w")
with open(temp, "r") as f:
    next(f)
    for line in f:
        line = line.strip("\n")
        info = line.split("\t")
        if line.startswith("#"):
            isolates = "\t".join(info[9:])
            temp2.write("\t"+isolates+"\n")
        elif not line.startswith("#"):
            snp = info[1]+"."+info[4]
            pheno = "\t".join(info[9:])
            temp2.write(snp+"\t"+pheno+"\n")
temp2.close()

# transpose table and write to output
output = open(outfile, "w")
with open(temp2file, "r") as f:
    df = pd.read_table(f, sep = "\t", index_col = 0, header = 0)
    (df.T).to_csv(outfile, sep="\t")

output.close()
os.remove(temp)
os.remove(temp2file)
