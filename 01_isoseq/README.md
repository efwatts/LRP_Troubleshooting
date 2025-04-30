# Iso-Seq for Isoform Discovery <br />
See PacBio's documentation for more detailed information on the Iso-Seq process. <br />

## Input files <br />
- `raw_reads.flnc.bam` from your PacBio data <br />
- `gencode__fasta` [Gencode](https://www.gencodegenes.org/) genome reference <br />

## Required installations: <br />
If you are running this on your local machine, please consult the [PacBio Iso-Seq documentation](https://github.com/PacificBiosciences/pbbioconda) for installation instructions. <br />
If you are using Rivanna or another HPC, you will need to load the following modules: <br />
```
module load isoseqenv/py3.7
module load gcc/11.4.0
module load bedops/2.4.41
module load nseg/1.0.0
module load bioconda/py3.10
module load smrtlink/13.1.0.221970
module load miniforge/24.3.0-py3.11
```

## Run Iso-Seq3 from a SLURM script <br />
Please note: this is a very memory-hungry step. If running multiple samples, you may need to increase the memory allocation more than expected. <br />
It is, however, recommended to run all of your samples at once for algorithmic purposes and for PB accession number harmonization. <br />
```
sbatch 00_scripts/01_isoseq.sh
```
## Or run these commands. <br />
```
# Merge samples
pbmerge -o 01_isoseq/merge/merged.flnc.bam /project/sheynkman/raw_data/PacBio/Sample-1-flnc.bam /project/sheynkman/raw_data/PacBio/Sample-2-flnc.bam /project/sheynkman/raw_data/PacBio/Sample-3-flnc.bam /project/sheynkman/raw_data/PacBio/Sample-4-flnc.bam /project/sheynkman/raw_data/PacBio/Sample-5-flnc.bam /project/sheynkman/raw_data/PacBio/Sample-6-flnc.bam

# Cluster reads
isoseq cluster2 01_isoseq/merge/merged.flnc.bam 01_isoseq/cluster/merged.clustered.bam

# Align reads to the genome 
pbmm2 align /project/sheynkman/external_data/GENCODE_v47/GRCh38.primary_assembly.genome.fa 01_isoseq/cluster/merged.clustered.bam 01_isoseq/align/merged.aligned.bam --preset ISOSEQ --sort -j 40 --log-level INFO

# Collapse redundant reads
isoseq collapse --do-not-collapse-extra-5exons 01_isoseq/align/merged.aligned.bam 01_isoseq/merge/merged.flnc.bam 01_isoseq/collapse/merged.collapsed.gff

conda deactivate
module purge
```

## Next go to [SQANTI module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/02_sqanti) or [Make Gencode Database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/02_make_gencode_database)
### Note: the [Reference Tables  module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_reference_tables) can be done at this stage as well. 

