#!/usr/bin/env/ python

import sys
from Bio import SeqIO

#####
# This script takes in DNA gyrase subunit B amino acid sequences from viridans
# group streptococci, and outputs a sepcies identification.
# Method from: Pena-Galloway, J., et al. "GyrB Polymorphisms Accurately Assign
# Invase Viridans Group Streptococcal Species".
# ** sequence IDs must not contain spaces (:%s/\ //g to remove spaces) **
#####

# check for correct arguments
if len(sys.argv) != 3:
	print("Usage: gyrBTyping.py <fasta file> <output file>")
	sys.exit(0)

InFileName = sys.argv[1]
OutFileName = sys.argv[2]

# create id#:species dictionary
species = {'9':'mitis','10':'oralis','11':'parasanguinis','19':'infantis','20':'australis','21':'sanguinis',\
'22':'anginosus','23':'constellatus','24':'salivarius','25':'vestibularis', '26':'Species cannot be determined by gyrB typing',\
'27':'Sequence is too short for analysis'}

# assign species via gyrB typing flow chart (see paper referenced above)
gyrb_ident = {}
for seq in SeqIO.parse(InFileName, "fasta"):
	if len(seq) >= 502:
		if seq[371-1] == 'M' and seq[503-1] == 'L':
			if seq[494-1] == 'S':
				gyrb_id = 9
			if seq[494-1] == 'T':
				gyrb_id = 10
		elif seq[371-1] in ('L','I','F') and seq[503-1] == 'I':
			if seq[494-1] == 'T':
				gyrb_id = 11
			if seq[425-1] == 'A':
				if seq[379-1] == 'R':
                        		gyrb_id = 19
				if seq[379-1] == 'K':
					gyrb_id = 20
			if seq[376-1] == 'V' and seq[423-1] == 'D':
				if seq[378-1] == 'R':
                        		gyrb_id = 21
				if seq[494-1] == 'S':
                        		gyrb_id = 22
                		if seq[494-1] == 'N':
					gyrb_id = 23
			if seq[424-1] == 'A' and seq[426-1] == 'M' and seq[427-1] == 'N' and seq[499-1] == 'H':
				if seq[489-1] == 'A':
                        		gyrb_id = 24
                		if seq[489-1] == 'S':
	                       		gyrb_id = 25
		else:	# if sequence doesnt match any of these classifications - "Species cannot
			# be determined by gyrB typing"
			gyrb_id = 26
	else:	# if sequence is not at least 503 residues - "Sequence is too short for analysis"
		gyrb_id = 27
	gyrb_ident[seq.id] = gyrb_id # add gyrB_id to seq.id in dictionary

# write species identities to output file
with open(OutFileName, 'w') as OutFile:
	OutFile.write('Sequence ID'+'\t'+'Streptococcus species'+'\n')
	for seq_id, species_ID in gyrb_ident.iteritems():
		OutFile.write(seq_id +'\t'+ species[str(species_ID)]+'\n')
