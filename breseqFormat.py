#!/usr/bin/env python

import sys

#####
# This script takes in GD files produced by Breseq's gdtools COMPARE function,
# and pads the structure so they are readable into Excel or R.
#####

if len(sys.argv) < 2:
	print("Usage: breseqFormat.py <compare1.gd> ... <compareN.gd>")
	sys.exit(0)

gds = sys.argv[1:]

for f in gds:
	with open(f,"r") as IN:
		with open(f.split(".")[0]+"_reformat.gd","w") as OUT:
			next(IN)
			for line in IN:
				line = line.strip()
				info = line.split("\t")
				try:
					if info[6].startswith("frequency"):
						newline = "\t".join(info[:6]+["\t"*6]+info[6:])
					else:
						newline = line
				except IndexError:
					pass
				OUT.write(newline+"\n")

