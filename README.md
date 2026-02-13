Motif Mark
===========

A Python script that finds motifs in sequences (FASTA) and draws a visual map
of genes with exons, introns and motif locations using Cairo.

Files
-----
- `motif-mark-oop.py` — main script (object-oriented plotting with `Sequence`, `Intron`, `Exon`, `Motif`).
- `bioinfo.py` — helper used by the script (expected to be present in the same directory).

Requirements
------------
- Python 3
- pycairo (the Python bindings for Cairo)
- The local `bioinfo.py` used by the project (kept in the repo)


Usage
-----
Run the script with a FASTA file and a motif list (one motif per line):

```bash
./motif-mark-oop.py -f Figure_1.fasta -m Fig_1_motifs.txt
```

Output
------
- The script writes a PNG file named after the FASTA file prefix (e.g. `Figure_1.png`) in the
	current working directory.
- The canvas size (width × height) auto-scales to the longest sequence and total number of genes.

Customization
-------------
- Motif colors: edit the `motif_colors` list near the top of `motif-mark-oop.py`.
- Motif transparency: change the alpha used in `Motif.plot_motif()` (uses `set_source_rgba`).
- Exon color: change the RGB in `Exon.plot_exon()`.
- Background: white background is painted when the Cairo surface is created.
- Surface sizing: the script computes width from the longest sequence and height from number of genes; if you want a different scale, modify the `surface_width`/`surface_height` calculation.

Legend
------
A legend is drawn on the right with a boxed border and the title "Motif" above the box. It uses the same colors assigned to motifs.

Example Run:
------
The output of 

```bash
./motif-mark-oop.py -f Figure_1.fasta -m Fig_1_motifs.txt
```
is this image (named Figure_1.png):

<img width="1021" height="440" alt="Figure_1" src="https://github.com/user-attachments/assets/d52c55f3-d180-44ce-8289-9e0a3eb1ebe0" />

