#!/usr/bin/env python

import bioinfo
import argparse
import cairo
import re

def get_args():
    parser = argparse.ArgumentParser(description="A program to find motifs in RNA or DNA sequencing data")
    parser.add_argument("-f", "--fasta_file", help="A fasta file", required=True)
    parser.add_argument("-m", "--motif_file", help="A text file with one motif per line", required=True)
    return parser.parse_args()

args = get_args()
fasta_file=args.fasta_file
motif_file=args.motif_file

class Sequence:
    def __init__ (self, nucl_seq, header):
        '''
        Object of class sequence. Introns and exons will be sequences
        '''
        ## Data ##
        self.seq = nucl_seq
        self.header = header
        self.length = len(nucl_seq)
    ## Methods ##
    def motif_search(self, seq, motif):
        # Dictionary for IUPAC degenerate bases
        iupac_DNA = {
            'A': 'A', 'C': 'C', 'G': 'G', 'T': 'T', 'U': 'U',
            'W': '[AT]', 'S': '[CG]', 'M': '[AC]', 'K': '[GT]',
            'R': '[AG]', 'Y': '[CT]', 'B': '[CGT]', 'D': '[AGT]',
            'H': '[ACT]', 'V': '[ACG]', 'N': '[ACGT]'
        }
        
        # Convert motif with degenerate bases to regex pattern
        regex_motif = ''
        for base in motif.upper():
            regex_motif += iupac_DNA.get(base, base)
        
        motif_pos = []
        pattern = re.compile(regex_motif, re.IGNORECASE)
        
        for match in pattern.finditer(seq):
            motif_pos.append(match.start())
        
        return motif_pos 
        
    def get_introns(self, seq):
        """
        Find all introns (lowercase regions) and return their start and end positions.
        Returns:
            List of tuples with (start_pos, end_pos) for each intron
        """
        introns = []
        for match in re.finditer("[a-z]+", seq):
            introns.append((match.start(), match.end()))
        return introns
    def get_exons(self, seq):
        """
        Find all exons (uppercase regions) and return their start and end positions.
        Returns:
            List of tuples with (start_pos, end_pos) for each exon
        """
        exons = []
        for match in re.finditer("[A-Z]+", seq):
            exons.append((match.start() + 1, match.end() - 1))
        return exons

class Intron(Sequence):
    def plot_intron(self, start_location, end_location):
        # Use cairo to plot the intron as a line between the start and end locations
        pass

class Exon(Sequence):
    def plot_exon(self, start_location, end_location):
        # Use cairo to plot the exon as a box between the start and end locations
        pass

class Motif:
    def __init__ (self, seq, location):
        '''
        Class for keeping the locations of the motif in the current gene.
        '''
        ## Data ##
        self.seq = seq
        self.pos = location
    def plot_motif(self, location):
        pass

with open(motif_file, "r") as motif_file:
    motif_list = []
    for line in motif_file:
        line = line.strip('\n')
        motif_list.append(line)

bioinfo.oneline_fasta(fasta_file, "oneline.fasta")
with open("oneline.fasta", "r") as fasta:
    for line in fasta:
        line = line.strip('\n')
        if line.startswith(">"):
            header = line
        else:
            nucl_seq = line
            seq_obj = Sequence(nucl_seq, header)
            introns = seq_obj.get_introns(nucl_seq)
            exons = seq_obj.get_exons(nucl_seq)
            #for motif in motif_list:
                #motif_locations = seq_obj.motif_search(nucl_seq, motif)
                #print(f'Motif {motif} found at positions: {motif_locations}')
            print(f"Sequence: {header}")
            print(f"introns: {introns}")
            print(f"exons: {exons}")
