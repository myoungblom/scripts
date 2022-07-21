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
		next(IN)
		with open(f.split(".")[0]+"_gd.tsv","w") as OUT:
			header = ["type","id","parent-id","reference","position","new_char","aa_new_seq","aa_position",\
					"aa_ref_seq","codon_new_seq","codon_number","codon_position","codon_ref_seq"]
			for line in IN:
				line = line.strip()
				info = line.split("\t")
				if info[0] != "UN":
					if info[6].startswith("frequency="):
						newinfo = info[:6]+[""]*7+info[6:17]+[""]+info[18:]
					elif info[7].startswith("frequency="):
						newinfo = info[:7]+[""]*6+info[7:18]+[""]+info[19:]
					elif info[8].startswith("frequency="):
						newinfo = info[:8]+[""]*5+info[8:19]+[""]+info[20:]
					else:
						newinfo = info
					if newinfo[1] == "1":
						for x in newinfo[13:]:
							head = x.split("=")[0]
							header.append(head)
						OUT.write("\t".join(header)+"\n")
					newline = newinfo[:6]
					for y in newinfo[6:]:
						try:
							tail = y.split("=")[1]
							newline.append(tail)
						except IndexError:
							newline.append(y)
					finalline = []
					for item in newline:
						if item == "":
							finalline.append("NA")
						else:
							finalline.append(item)
					OUT.write("\t".join(finalline)+"\n")

