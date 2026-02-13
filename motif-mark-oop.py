#!/usr/bin/env python

import bioinfo
import argparse
import cairo
import re

# Color palette for motifs only works for upt to 8 motifs at the moment
# This maybe could be randomized to allow for as many motifs as you want but I didn't want to.
# If there are more than 8 motifs, the colors will just repeat
motif_colors = [
    (0, 0, 1),        # Blue
    (0, 1, 1),        # Cyan
    (1, 0, 1),        # Magenta
    (0, 1, 0),        # Green
    (1, 1, 0),        # Yellow
    (1, 0, 0),        # Red
    (0.5, 0, 1),      # Purple
    (1, 0.5, 0),      # Orange
]

def get_motif_color(index):
    """Get a unique color for each motif"""
    return motif_colors[index % len(motif_colors)]

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
            'A': 'A', 'C': 'C', 'G': 'G', 'T': '[TU]', 'U': '[UT]',
            'W': '[ATU]', 'S': '[CG]', 'M': '[AC]', 'K': '[GTU]',
            'R': '[AG]', 'Y': '[CTU]', 'B': '[CGTU]', 'D': '[AGTU]',
            'H': '[ACTU]', 'V': '[ACG]', 'N': '[ACGTU]'
        }
        # Convert motif with degenerate bases to regex pattern
        # This actually also will handle RNA
        regex_motif = ''
        for base in motif.upper():
            regex_motif += iupac_DNA.get(base, base)
        motif_pos = set()
        look = re.compile(r'(?={})'.format(regex_motif), re.IGNORECASE)
        for m in look.finditer(seq):
            motif_pos.add(m.start()+1)
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
    def plot_headers(self, context, gene_num, header):
        '''
        Plot the header line for each gene as the title for the gene/motif plot.
        '''
        context.set_source_rgb(0, 0, 0)  # Black
        context.set_font_size(14)
        y_pos = gene_num * 96 - 40
        context.move_to(10, y_pos)
        context.show_text(self.header)
    def plot_legend(self, context, motif_list):
        '''
        Plot the legend for the figure. Colors are set for each motif.
        '''
        context.set_source_rgb(0, 0, 0) 
        context.set_font_size(14)
        y_pos = len(motif_list)+30
        # Title for the legend
        context.set_source_rgb(0, 0, 0)
        context.move_to(surface_width - 120, y_pos - 10)
        context.show_text("Motif")
        # reset font size for items (making them a little smaller)
        context.set_font_size(12)
        for motif_index, motif in enumerate(motif_list):
            motif_color = get_motif_color(motif_index)
            context.set_source_rgb(*motif_color)
            context.rectangle(surface_width - 140, y_pos + motif_index * 20, 10, 10)
            context.fill()
            context.set_source_rgb(0, 0, 0)
            context.move_to(surface_width - 120, y_pos + motif_index * 20 + 10)
            context.show_text(motif)

class Intron(Sequence):
    def plot_intron(self, context, start_location, end_location, gene_num):
        '''
        Draw intron as a black line between start and end. 
        Gene_num is used to determine the y position of the line.
        '''
        context.set_source_rgb(0, 0, 0)  # Black
        context.set_line_width(2)
        y_pos = gene_num * 96 # 96 gives it nice spacing between genes
        context.move_to(start_location+50, y_pos)
        context.line_to(end_location+50, y_pos)
        context.stroke()

class Exon(Sequence):
    def plot_exon(self, context, start_location, end_location, gene_num):
        ''' 
        Draw exon as a filled gray rectangle between start and end. 
        Gene_num is used to determine the y position of the rectangle.
        '''
        y_pos = gene_num * 96
        width = end_location - start_location
        context.set_source_rgb(0.4, 0.4, 0.4)
        context.rectangle(start_location+49, y_pos-10, width+2, 20)
        context.fill()

class Motif:
    def __init__ (self, motif_seq, location, color=(1, 0, 0)):
        '''
        Class for plotting the locations of the motif in the current gene.
        '''
        ## Data ##
        self.pos = location
        self.len = len(motif_seq)
        self.color = color
    def plot_motif(self, context, gene_num):
        y_pos = gene_num * 96
        context.set_source_rgba(*self.color, 0.7)  #70% transparency
        context.rectangle(self.pos+49, y_pos-10, self.len, 20)
        context.fill()

# Create a list of motifs from the motif file
with open(motif_file, "r") as motif_file:
    motif_list = []
    for line in motif_file:
        line = line.strip('\n')
        motif_list.append(line)

# Convert the FASTA file to oneline format for easier parsing
bioinfo.oneline_fasta(fasta_file, "oneline.fasta")

# Count the number of genes and find the longest sequence in the FASTA file
# This will be used to create the dimensions of the overall figure
num_genes = 0
max_seq_length = 0
with open("oneline.fasta", "r") as fasta:
    for line in fasta:
        line = line.strip('\n')
        if line.startswith(">"):
            num_genes += 1
        else:
            max_seq_length = max(max_seq_length, len(line))

# Get surface dimensions based on number of genes and longest sequence
# Height: 96 pixels per gene + 56 pixels padding
# Width: 1 pixel per base + 250 pixels padding (250 is for the legend and some extra space on the right)
surface_height = max(100, num_genes * 96 +56)
surface_width = max(100, max_seq_length + 250)

# Create the cairo surface and context, and plot the genes, motifs, and legend
with open("oneline.fasta", "r") as fasta:
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, surface_width, surface_height)
    context = cairo.Context(surface)
    # Set white background for the figure
    context.set_source_rgb(1, 1, 1)
    context.paint()
    gene_num = 0
    for line in fasta:
        line = line.strip('\n')
        if line.startswith(">"):
            header = line
            gene_num += 1      # This will be used to get the vertical positions and spacing  
        else:
            nucl_seq = line
            seq_obj = Sequence(nucl_seq, header)
            seq_obj.plot_headers(context, gene_num, header)
            introns = seq_obj.get_introns(nucl_seq)
            for intron in introns:
                intron_obj = Intron(nucl_seq, header)
                intron_obj.plot_intron(context, intron[0], intron[1], gene_num)
            exons = seq_obj.get_exons(nucl_seq)
            for exon in exons:
                exon_obj = Exon(nucl_seq, header)
                exon_obj.plot_exon(context,exon[0], exon[1], gene_num)
            for motif_index, motif in enumerate(motif_list):
                motif_color = get_motif_color(motif_index)
                motif_locations = seq_obj.motif_search(nucl_seq, motif)
                #print(f"gene: {header}, motif: {motif}, locations: {motif_locations}")  
                motif_len = len(motif)  
                for motif_location in motif_locations:
                    # if motif == "YYYYYYYYYY":
                    #     print(f"Gene: {header}, Location: {motif_location}")  # Print motif location for debugging
                    motif_obj = Motif(motif, motif_location, motif_color)
                    motif_obj.plot_motif(context, gene_num)
    seq_obj.plot_legend(context, motif_list)
    fasta_name = fasta_file.split(".")[0]
    surface.write_to_png(f"{fasta_name}.png")
# Tada!
