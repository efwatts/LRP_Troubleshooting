# Track Visualization
Prepare data to be viewed in [UCSC Genome Browser](https://genome.ucsc.edu/). Here, we color code by sample and CPM, with the major protein isoform being a darker color than the other. The major isoform is the one with the highest CPM. <br />

Here is an AI generated summary of this step: <br />
> The `17_track_visualization` module is designed to create visualizations for protein and peptide tracks in the UCSC Genome Browser. It takes as input various GTF files, including GENCODE, CDS, and hybrid databases, along with peptide data from MetaMorpheus. The module generates BED12 files for both protein and peptide tracks, as well as multiregion BED files for refined, filtered, and hybrid databases. The output files are organized into directories for easy access and visualization in the UCSC Genome Browser.
## Input files
- `cds.gtf` - GTF file with CDS annotations for each sample. This file is generated from the [07 Make CDS GTF module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/07_make_cds_gtf).

_Optional:_
- `filtered_cds.gtf` - filtered GTF file for each sample. This file is generated from the [13 Protein Filter module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/13_protein_filter)
- `hybrid_cds.gtf` - hybrid GTF file for each sample. This file is generated from the [14 Protein Hybrid Database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/14_protein_hybrid_database)
## Required installations
Load modules (if on HPC) and create and activate conda environment. <br />
```
module load gcc/11.4.0 openmpi/4.1.4
module load python/3.11.4
module load miniforge/24.3.0-py3.11

conda env create -f 00_environments/visualization.yml
conda activate visualization
```
## Run Track Visualization from a SLURM script
```
sbatch 00_scripts/17_track_visualization.sh
```
## Or run these commands.
```
# Condition 1
gtfToGenePred 07_make_cds_gtf/condition1_cds.gtf 17_track_visualization/condition1.genePred
genePredToBed 17_track_visualization/condition1.genePred 17_track_visualization/condition1.bed12

python 00_scripts/17_rgb_by_cpm_to_bed.py --input_bed 17_track_visualization/condition1.bed12 --day condition1 --output_file 17_track_visualization/condition1.bed12

# Condition 2
gtfToGenePred 07_make_cds_gtf/condition2_cds.gtf 17_track_visualization/condition2.genePred
genePredToBed 17_track_visualization/condition2.genePred 17_track_visualization/condition2.bed12

python 00_scripts/17_rgb_by_cpm_to_bed.py --input_bed 17_track_visualization/condition2.bed12 --day condition2 --output_file 17_track_visualization/condition2.bed12

conda deactivate
module purge
```
## Proceed to [18_SUPPA](https://github.com/efwatts/LRP_Troubleshooting/tree/main/18_SUPPA)