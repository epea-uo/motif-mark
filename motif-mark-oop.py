#!/usr/bin/env python

import bioinfo
import argparse
import cairo

def get_args():
    parser = argparse.ArgumentParser(description="A program to find motifs in RNA or DNA sequencing data")
    parser.add_argument("-f", "--fasta_file", help="A fasta file", required=True)
    parser.add_argument("-m", "--motif_file", help="A text file with one motif per line", required=True)
    return parser.parse_args()

args = get_args()
fasta_file=args.fasta_file
motif_file=args.motif_file

class Sequence:
    def __init__ (self, nucl_seq):
        '''
        Object of class sequence. Introns and exons will be sequences
        '''
        ## Data ##
        self.seq = nucl_seq
        self.length = len(nucl_seq)
    ## Methods ##
    def motif_search(self,seq, motif_list):
        blablablabla
    def get_introns(self):
        dkvjbkdvn
    def get_exons(self):
        dkjbdkjbv

class Motif:
    def __init__ (self, seq, location):
        '''
        Class for keeping the locations of the motif in the current gene.
        '''
        ## Data ##
        self.seq = seq
        self.pos = location

motif_list = []
for line in motif_file:
    line = line.strip('\n')
    motif_list += line


