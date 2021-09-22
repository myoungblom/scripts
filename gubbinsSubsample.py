#!/usr/bin/env python3

import sys
from Bio import SeqIO
import subprocess as sp

#####
#
#####

if len(sys.argv) != 4:
	print("Usage: gubbinsSubsample.py <full-aln> <totalSeqs> <subSampleSize>")
	sys.exit(0)

fasta = sys.argv[1]
total = sys.argv[2]
sub = sys.argv[3]

# get alignment length
lengths = []
for seq in SeqIO.parse(fasta,"fasta"):
	lengths.append(len(seq.seq))

if len(set(lengths)) > 1:
	print("Error: sequences are of different lengths - check input data")
	sys.exit(0)
else:
	seqLength = str(lengths[0])

# make empty placeholder file
sp.call(['touch','placeholder.txt'])

# subsample alignment 50X
outProp = open("proportionAlnAffected.txt","w")
for n in range(1,51):
	outfile = str(n)+"_subsampled.aln"
	gff = outfile.split(".")[0]+".recombination_predictions.gff"
	gubbins_out = str(n)+"_gubbins_tabular.txt"
	pr_out = str(n)+"_perc_recomb.txt"
	sp.call(['python','randomSubsampleFasta_MAY.py','-t',total,'-s',sub,fasta]) #subsample
	sp.call(['mv','subsampled.fasta',outfile]) #rename
	sp.call(['run_gubbins.py','--threads','8',outfile]) #run gubbins on subsampled alignment
	sp.call(['python','compareGubbinsBNG.py','-f','placeholder.txt',gff]) #reformat gubbins output
	sp.call(['mv','gubbins_tabular.txt',gubbins_out]) #rename
	sp.call(['python','proportionAlignmentAffected.py',gubbins_out,seqLength],stdout=outProp) #calc proportion of alignment affected
	sp.call('rm '+str(n)+"_subsampled*", shell=True) #remove extra gubbins files
	sp.call('rm '+gubbins_out, shell=True)

outProp.close()
