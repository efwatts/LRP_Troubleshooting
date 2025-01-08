### Step 1: Filtering with `03_filter_sqanti.py`
- **Input:**
  - A SQANTI classification table (--sqanti_classification).
  - GTF and FASTA files for corrected transcripts.
  - Optionally, files for protein-coding genes and gene identifiers (--protein_coding_genes and --ensg_gene).
- **Processing:**
  - Filters the classification table based on user-specified criteria.
  - Filters the GTF and FASTA files to include only the isoforms passing the filters.
- **Output:**
  - A filtered classification table (filtered_<input_name>.tsv).
  - Filtered GTF and FASTA files.

### Step 2: Collapsing Isoforms with `03_collapse_isoforms.py`
- **Input:**
The filtered GTF and FASTA files from Step 1.
- **Processing:**
  - Groups isoforms by their PB cluster ID.
  - Collapses redundant isoforms based on exon structure and junctions.
  - Produces collapsed GTF and FASTA files.
- **Output:**
  - A collapsed GFF file (e.g., name_corrected.5degfilter.gff).
  - A collapsed FASTA file (e.g., name_corrected.5degfilter.fasta).

### Step 3: Final Filtering with 
- **Input:**
  - The filtered FASTA file from Step 1.
  - The filtered classification table.
- **Processing:**
  - Extracts sequence IDs from the filtered FASTA file.
  - Further filters the classification table to include only the matching sequence IDs.
- **Output:**
  - A refined classification table (<name>_classification.5degfilter.tsv).
