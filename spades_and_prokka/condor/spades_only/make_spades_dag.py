#!/usr/bin/env python
#This script will take an input text file and a dag template and output a dag for 
#denovo assembly and annotation. For each sample, a tab-delimited .txt file is required containing:
#SRAReadGroupID     SampleGroupID     LibraryID       SeqPlatform     paired/single
#ERR071082       ERS088906       ERX048850       illumina        paired

import sys
import os
import argparse
from string import Template

    
def get_args():    
    parser = argparse.ArgumentParser(description='Pipeline for denovo assembly & annotation')
    parser.add_argument("input", help="File describing read data information")
    parser.add_argument("dagtemplate", help="dag template")
    return parser.parse_args()

args = get_args()

with open(args.dagtemplate, "r") as template_file:
    template = Template(template_file.read())

with open(args.input, 'r') as infile:
    outfileName = args.input.split(".")[0] + "_toplevel.dag"
    with open(outfileName, "w") as outfile:
        for line in infile:
            line = line.strip()
            inputList = line.split()
            variableMap = {}
            variableMap['run'] = inputList[0]
            with open("{0}_SPAdes.dag".format(variableMap['run']), "w") as dagfile:
                out = template.substitute(variableMap)
                dagfile.write(out)
            outfile.write("SPLICE {0} {0}_SPAdes.dag\n".format(variableMap['run']))
