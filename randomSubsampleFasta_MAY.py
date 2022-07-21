#!/usr/bin/env python

import sys
import os
from Bio import SeqIO
import argparse
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC,Gapped
import numpy as np

###############
# This script randomly subsamples an aln
##################

def get_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='subsample fasta')
    parser.add_argument("input_fasta", help="OG fasta aln")
    parser.add_argument("-t", help="number of sequences in full alignment",type=int)
    parser.add_argument("-s",help="number of sequences in subsampled alignment",type=int)
    return parser.parse_args()

def remove_isolates(toKeep_list,input_fasta):
    """this removes isolates from the fasta and saves them as individual fastas"""
    sequences_to_keep = []
    tot_sequences = []
    for seq_record in SeqIO.parse(input_fasta, "fasta"):
        tot_sequences.append(seq_record)
    print(toKeep_list)
    for i,seq_record in enumerate(tot_sequences):
        print i
        if i not in toKeep_list:
            print("removed "+seq_record.id)
        else:
            sequences_to_keep.append(seq_record)
    return sequences_to_keep

def print_out_aln(keepList,out_handle):
    output_handle = open(out_handle,"w")
    SeqIO.write(keepList, output_handle, "fasta")
    output_handle.close()

args = get_args()

Start = 0
Stop = args.t - 1 
limit = args.s

randomKeepList = np.random.choice(Stop,limit,replace = False)
seq_to_keep_list = remove_isolates(randomKeepList, args.input_fasta)
print_out_aln(seq_to_keep_list,"subsampled.fasta")


