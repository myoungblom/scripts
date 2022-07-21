#!/usr/bin/env/ python
import sys

#####
# This script takes in a fasta file of nucleotide sequences, and returns
# a file containing the forward and reverse translations of all sequences,
# in all 3 frames.
#####

# check for correct command line arguments
if len(sys.argv) != 2:
	print("Usage: translate.py  <fasta file>")
	sys.exit(0)

inFileName = sys.argv[1]
outFileName = inFileName.split(".")[0]+"_translated.fasta"

# reverse complement dictionary
rev_comp = {'a':'t','t':'a','g':'c','c':'g'}

# define reverse complement function
def reverse_complement(sequence):
	rev_seq = []
	for base in sequence[::-1]:
		rev_seq.append(rev_comp[base])
	return(''.join(rev_seq))

# codon table as a dictionary
codon_dict = {\
'ttt':'F','ttc':'F','tta':'L','ttg':'L','ctt':'L',\
'ctc':'L','cta':'L','ctg':'L','att':'I','atc':'I',\
'ata':'I','atg':'M','gtt':'V','gtc':'V','gta':'V',\
'gtg':'V','tct':'S','tcc':'S','tca':'S','tcg':'S',\
'cct':'P','ccc':'P','cca':'P','ccg':'P','act':'T',\
'acc':'T','aca':'T','acg':'T','gct':'A','gcc':'A',\
'gca':'A','gcg':'A','tat':'Y','tac':'Y','taa':'*',\
'tag':'*','cat':'H','cac':'H','caa':'Q','cag':'Q',\
'aat':'N','aac':'N','aaa':'K','aag':'K','gat':'D',\
'gac':'D','gaa':'E','gag':'E','tgt':'C','tgc':'C',\
'tga':'*','tgg':'W','cgt':'R','cgc':'R','cga':'R',\
'cgg':'R','agt':'S','agc':'S','aga':'R','agg':'R',\
'ggt':'G','ggc':'G','gga':'G','ggg':'G'}

# define function to translate sequences
def translate(sequence, start):
	protein_seq = ''
	add = True
	for base in range(start, len(sequence), 3):
		if add == True:
			codon = (sequence[base:base+3]).lower()
			if len(codon) == 3:
				if codon_dict[codon] == "*":
					add = False
					protein_seq += codon_dict[codon]
				else:
					protein_seq += codon_dict[codon]
	return protein_seq

# read in fasta file to dictionary
fasta = dict()
with open(inFileName, 'r') as f:
	first = True
	seq = ''
	for line in f:
		line = line.rstrip('\n')
		if line.startswith('>'):
			if first == False:
				fasta[header] = seq
				seq = ''
			header = line
			first = False
		else:
			seq = seq+line.lower()
	fasta[header] = seq

# make reverse complement of sequences, translate both directions in all 3 frames and write to output
with open(outFileName, 'w') as output:
	for header, seq in fasta.items():
		forward_seq = seq
		reverse_seq = reverse_complement(seq)
		F1 = translate(forward_seq, 0)
		F2 = translate(forward_seq, 1)
		F3 = translate(forward_seq, 2)
		R1 = translate(reverse_seq, 0)
		R2 = translate(reverse_seq, 1)
		R3 = translate(reverse_seq, 2)
		output.write(header+"_F1\n"+F1+"\n")
		#output.write(header+"_F2\n"+F2+"\n")
		#output.write(header+"_F3\n"+F3+"\n")
		#output.write(header+"_R1\n"+R1+"\n")
		#output.write(header+"_R2\n"+R2+"\n")
		#output.write(header+"_R3\n"+R3+"\n")
