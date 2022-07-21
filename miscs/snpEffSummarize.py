#!/usr/bin/python

import sys

#####
# This script takes in an annotated vcf from SnpEff and outputs a summary file with mutation consequences.
#####

# check for correct command-line arguments
if len(sys.argv) != 2:
    print("Usage: snpEffSummary.py <snpEff.vcf>")
    sys.exit(0)

vcf = sys.argv[1]
out = vcf.strip(".vcf")+"_summary.txt"

with open(out, "w") as output:
    output.write("mut\tconsequence\taa\timpact\n")
    with open(vcf, "r") as f:
        for line in f:
            if not line.startswith("#"):
                line = line.strip("\n")
                info = line.split("\t")
                annot = info[7].split("|")
                mut = info[3]+info[1]+info[4]
                con = annot[1]
                if con == "missense_variant":
                    aa = annot[10].split(".")[1]
                else:
                    aa = "NA"
                imp = annot[2]
                output.write(mut+"\t"+con+"\t"+aa+"\t"+imp+"\n")

