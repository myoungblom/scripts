#!/usr/bin/env python

import sys
import argparse
import os
from Bio import AlignIO
from Bio import SeqIO
import egglib
import subprocess
import numpy as np

#####
# This script takes in a core genome alignment, a gene presence absence csv
# and a list of EAI/DCC designations and randomly subsamples each group (sample size N, taken X times) 
# while calculating the number of segregating sites within the sample and the pangenome size.
#####

def get_arguments():
	"""
	Handle the command line arguments.
	"""
	parser = argparse.ArgumentParser(description="Random subsampling of alignment with calculation of # segregating sites \
	and pangenome size.")
	parser.add_argument("alignment",help="alignment (usually core genome alignment from Roary)")
	parser.add_argument("gpa",help="gene presence absence csv from Roary")
	parser.add_argument("eai_dcc_list",help="tab separated file with list of isolates and their EAI/DCC designations")
	parser.add_argument("-N",default=10,type=int,help="subsample size. default=10")
	parser.add_argument("-X",default=100,type=int,help="number of times to subsample each group. default=100")
	return parser.parse_args()


def make_group_lists(listfile):
	"""
	Make a dictionary of isolate types (EAI, DCC1 or DCC2).
	"""
	eaiDccDict = {"EAI":[],"DCC1":[],"DCC2":[]}
	with open(listfile, "r") as f:
		next(f)
		for line in f:
			iso = line.strip().split("\t")[0]
			iso_type = line.strip().split("\t")[1]
			eaiDccDict[iso_type].append(iso)
	return eaiDccDict

def make_gpa_dict(gpafile):
	"""
	Turn a gene presence absence file into a dictionary.
	"""
	gpaDict = {}
	with open(gpafile,"r") as f:
		next(f)
		for line in f:
			info = line.strip().split(",")
			gene = info[0]
			gpaDict[gene] = []
			gpas = info[14:]
			for iso in gpas:
				if iso != "":
					gpaDict[gene].append(iso.split("_")[0])
	return gpaDict

def calc_stats(alnfile):
	"""
	Calculate number of segregating sites of a given alignment two different ways.
	"""
	sDict = {}
	# calc S using egglib
	cs = egglib.stats.ComputeStats()
	cs.add_stats('S')
	a = egglib.io.from_fasta(alnfile)
	polyDict = cs.process_align(a, filtr=egglib.stats.filter_default)
	sDict['egglib'] = polyDict['S']
	# calc S using snp sites
	subprocess.call(['/opt/PepPrograms/snp_sites-2.0.3/src/snp-sites','-m','-o','snp_sites.tmp',alnfile])
	snp_aln = AlignIO.read("snp_sites.tmp","fasta")
	sDict["snpsites"] = len(snp_aln[1].seq)
	os.remove("snp_sites.tmp")
	return sDict

def calc_pangenome_size(isoList, gpaDict):
	"""
	Given a list of isolates and a gene presence absence dictionary, calculate the size of the pangenome\
	of the sample.
	"""
	pangenome = 0
	isoSet = set(isoList)
	for key, value in gpaDict.items():
		geneSet = set(value)
		if isoSet.issubset(geneSet):
			pangenome += 1
	return pangenome

def pangenome_subsample(alnfile,isoList,N,outfile):
	"""
	Randomly selects N isolates from an isolate list and writes to multifasta file.
	"""
	out = open(outfile, "w")
	subsample = list(np.random.choice(isoList, size=N, replace=False))
	subsample_fastas = []
	for seq in SeqIO.parse(alnfile,"fasta"):
		if seq.id in subsample:
			subsample_fastas.append(seq)
	SeqIO.write(subsample_fastas, out, "fasta")
	out.close()
	return subsample
	

args = get_arguments()
types = make_group_lists(args.eai_dcc_list)
gpas = make_gpa_dict(args.gpa)

outputDict = {}

for iso_type,iso_list in types.items():
	if len(iso_list) != 0:
		for i in range(args.X):
			tmpfile = str(i)+".tmp"
			t = iso_type
			l = pangenome_subsample(args.alignment, iso_list, args.N, tmpfile)
			p = calc_pangenome_size(l, gpas)
			s = calc_stats(tmpfile)
			outputDict[t+"_"+str(i)] = [t,str(s["egglib"]),str(s["snpsites"]),str(p),",".join(l)]

with open("pangenome_segsites.txt","w") as out:
	out.write("type\tegglibS\tsnpsitesS,pangenomeSize,subsample\n")
	for key, value in outputDict.items():
		out.write("\t".join(value)+"\n")

os.remove("*.tmp")
