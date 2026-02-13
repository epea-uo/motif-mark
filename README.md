Motif Mark
===========

A small Python script that finds motifs in sequences (FASTA) and draws a visual map
of genes with exons, introns and motif locations using Cairo.

Files
-----
- `motif-mark-oop.py` — main script (object-oriented plotting with `Sequence`, `Intron`, `Exon`, `Motif`).
- `bioinfo.py` — helper used by the script (expected to be present in the same directory).
- Example FASTA and motif files may be named like `Figure_1.fasta` and `Fig_1_motifs.txt`.

Requirements
------------
- Python 3
- pycairo (the Python bindings for Cairo)
	- Debian/Ubuntu: `sudo apt install python3-cairo`
	- or via pip: `pip install pycairo`
- The local `bioinfo.py` used by the project (kept in the repo)

Quick install (recommended inside a virtualenv)
---------------------------------------------
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install pycairo
```

Usage
-----
Run the script with a FASTA file and a motif list (one motif per line):

```bash
python3 motif-mark-oop.py -f Figure_1.fasta -m Fig_1_motifs.txt
```

Output
------
- The script writes a PNG file named after the FASTA file prefix (e.g. `Figure_1.png`) in the
	current working directory.
- The canvas size (width × height) auto-scales to the longest sequence and number of genes.

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

Troubleshooting
---------------
- If you see an import error for Cairo, ensure `pycairo` is installed and you're using the same Python interpreter.
- If `bioinfo.py` is missing, place the helper file in the same directory or adjust the import path.

Next steps
----------
If you want, I can:
- Add an option to change output filename/path via CLI
- Save SVG instead of PNG for scalable output
- Add sample files and a small test harness

License
-------
MIT (or adapt to your preferred license)