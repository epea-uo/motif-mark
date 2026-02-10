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

