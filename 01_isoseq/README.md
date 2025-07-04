# Iso-Seq for Isoform Discovery <br />
See PacBio's documentation for more detailed information on the Iso-Seq process. <br />

## Input files <br />
- `raw_reads.flnc.bam` from your PacBio data <br />
- `gencode__fasta` [Gencode](https://www.gencodegenes.org/) genome reference <br />

If your `flnc.bam` files are the result of samples that were run separately and not demultiplexed, you will need to add identifiers to the bam files. <br />
For example, if you have 6 samples, you can run the following command to add identifiers:
```
for f in 00_input_data/*.bam; do
  base=$(basename "$f" .bam)
  samtools addreplacerg -r ID:"$base" -r SM:"$base" -o "00_input_data/subset_bams/${base}.rg.bam" "$f"
done
```

## Required installations: <br />
If you are running this on your local machine, please consult the [PacBio Iso-Seq documentation](https://github.com/PacificBiosciences/pbbioconda) for installation instructions. <br />
If you are using Rivanna or another HPC, you will need to load the following modules: <br />
```
module load isoseqenv
module load gcc
module load bedops
module load nseg
module load bioconda
module load smrtlink
module load miniforge
module load samtools
```
If you are not using Rivanna or an HPC that has Iso-Seq and SMRTLink pre-loaded, you may need to install the following conda packages: <br />
```
conda install -c bioconda isoseq pbtk pbmm2 lima
```
## Run Iso-Seq3 from a SLURM script <br />
Please note: this is a very memory-hungry step. If running multiple samples, you may need to increase the memory allocation more than expected. <br />
It is, however, recommended to run all of your samples at once for algorithmic purposes and for PB accession number harmonization. <br />
We ran some test on the `collapse` step and found that to reduce redundant transcripts but also capture real novel transcripts, we prefer to set the `--max-fuzzy-junction` to 0, `--max-5p-diff` to 50, and `--max-3p-diff` to 100. <br />
```
sbatch 00_scripts/01_isoseq.sh
```
## Or run these commands. <br />
Note: If your samples are all in the same directory, you can run this simplified `pbmerge` command `pbmerge -o 01_isoseq/merge/merged.flnc.bam $(find 00_input_data -name "*.bam")`
```
# Merge samples
pbmerge -o 01_isoseq/merge/merged.flnc.bam /project/sheynkman/raw_data/PacBio/Sample-1-flnc.bam /project/sheynkman/raw_data/PacBio/Sample-2-flnc.bam /project/sheynkman/raw_data/PacBio/Sample-3-flnc.bam /project/sheynkman/raw_data/PacBio/Sample-4-flnc.bam /project/sheynkman/raw_data/PacBio/Sample-5-flnc.bam /project/sheynkman/raw_data/PacBio/Sample-6-flnc.bam

# Cluster reads
isoseq cluster2 01_isoseq/merge/merged.flnc.bam 01_isoseq/cluster/merged.clustered.bam

# Align reads to the genome 
pbmm2 align /project/sheynkman/external_data/GENCODE_v47/GRCh38.primary_assembly.genome.fa 01_isoseq/cluster/merged.clustered.bam 01_isoseq/align/merged.aligned.bam --preset ISOSEQ --sort -j 40 --log-level INFO

# Collapse redundant reads
# Default: max fuzzy junctions 5, max 5p diff 50 max 3p diff 100
isoseq collapse --max-fuzzy-junction 0 --max-5p-diff 100 --max-3p-diff 200 01_isoseq/align/merged.aligned.bam 01_isoseq/merge/merged.flnc.bam 01_isoseq/collapse/merged.collapsed.gff

conda deactivate
module purge
```

## Next go to [SQANTI module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/02_sqanti) or [Make Gencode Database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/02_make_gencode_database)
### Note: the [Reference Tables  module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_reference_tables) can be done at this stage as well. 

