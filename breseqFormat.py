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
		with open(f.split(".")[0]+"_gd.csv","w") as OUT:
			header = ["type","id","parent-id","reference","position","new_char"]
			for line in IN:
				line = line.strip()
				info = line.split("\t")
				if info[0] != "UN":
					if info[6].startswith("frequency="):
						newinfo = info[:6]+[""]*7+info[6:]
					elif info[7].startswith("frequency="):
						newinfo = info[:7]+[""]*6+info[7:]
					elif info[8].startswith("frequency="):
						newinfo = info[:8]+[""]*5+info[8:]
					else:
						newinfo = info
					if newinfo[1] == "1":
						for x in newinfo[6:]:
							head = x.split("=")[0]
							header.append(head)
						OUT.write(",".join(header)+"\n")
					newline = newinfo[:6]
					for y in newinfo[6:]:
						try:
							tail = y.split("=")[1]
							newline.append(tail)
						except IndexError:
							newline.append(y)
					OUT.write(",".join(newline)+"\n")

