#!/usr/bin/env python

import sys

#####
# Companion script to alleleFreq.sh, takes in filtered vcf files from
# a single isolate sequenced at multiple time points, and tabulates
# mutation frequencies at each point.
# Filters:
#   - filters out mutations in regions specified by bed file
#   - filters out fixed (>95%) mutations relative to the reference
#   - filters out positions that remain WT at all sequenced timepoints
#####

if len(sys.argv) < 4:
	print("Usage: alleleFreq.py <strain.name> <bed file> <vcf1> <vcf2> ... <vcfN")
	sys.exit(0)

strain = sys.argv[1]
bed = sys.argv[2]
vcfs = sys.argv[3:]


def getBedCoor(bedfile):
    print("Parsing bed file ...")
    bedCoor = []
    with open(bedfile, "r") as f:
        for line in f:
            line = line.strip()
            info = line.split("\t")
            for i in range(int(info[1]), int(info[2])+1):
                bedCoor.append(i)
    return(bedCoor)

def filterMuts(vcf_list, dict_out, filter):
    file_count = 0
    for vcf in vcf_list:
        file_count += 1
        with open(vcf,"r") as f:
            count = 0
            print("Tabulating mutants from "+ vcf)    
            for line in f:                    
                if not line.startswith("#"):  
                    line = line.strip()
                    info = line.split("\t")
                    pos = info[1]
                    if pos not in filter:
                        count += 1
                        if count % 100000 == 0:
                            print(str(count)+" mutations processed")
                        ref = info[3]
                        alt = info[4].split(",")[0]
                        counts = info[9]
                        alleles = counts.split(":")[3]
                        refC = int(alleles.split(",")[0])
                        altC = int(alleles.split(",")[1])
                        if (altC > 5) and (refC >5):
                            total = refC+altC
                            if altC != 0:
                                altF = round((altC/total)*100,0)
                            else:
                                altF = 0
                            mut = "_".join([str(pos),ref,alt])
                            if mut not in dict_out.keys():
                                dict_out[mut] = [0]*(file_count-1)+[altF]
                            else:
                                dict_out[mut].append(altF)
        for key,value in dict_out.items():
            if len(value) == file_count-1:
                dict_out[key].append(0)
    return dict_out

freqs = {}
header = ["position","ref","alt"]
bad_coordinates = getBedCoor(bed)

for x in vcfs:
    header.append(x.split(".")[0])

filterMuts(vcfs, freqs, bad_coordinates)

print("Done tabulating mutations from all samples")

with open(strain+"_alleleFreqs.csv","w") as out:
    print("Filtering mutations ...")
    out.write(",".join(header)+"\n")
    for key,value in freqs.items():
        times = len(value)
        if (value.count(0) != times) and (not all(i >= 95 for i in value)) and (not all(i <= 20 for i in value)):
            info = key.split("_")
            pos = str(info[0])
            ref = info[1]
            alt = info[2]
            value_int = [str(x) for x in value]
            newinfo = [pos,ref,alt]+value_int
            newline = ",".join(newinfo)
            out.write(newline+"\n")