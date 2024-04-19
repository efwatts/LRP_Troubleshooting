# Iso-Seq 

## Required installations: <br />
Create a conda environment for this module (future iterations of the pipeline will likely have one base environment, but for now, each module has its own environment. Use the `isoseq_environment.yml` file in this module by running `conda env create -f isoseq_environment.yml`. To activate type `conda activate isoseq_env`. You may also need to install [SMRT Link](https://www.pacb.com/support/software-downloads/).

## Run Iso-Seq3 from a script or command line (see below for a breakdown of the steps) <br />
If using Rivanna or other HPC, use the script `01_isoseq.sh`, otherwise run these commands. <br />
```
cd /project/sheynkman/users/emily/LRP_test/jurkat

conda activate isoseq_env

pbindex ./00_input_data/jurkat_merged.ccs.bam

bamtools filter -tag 'rq':'>=0.90' -in ./00_input_data/jurkat_merged.ccs.bam -out ./01_isoseq/filter/filtered.merged.bam

# Find and remove adapters/barcodes
lima --isoseq --dump-clips --peek-guess -j 4 ./01_isoseq/filter/filtered.merged.bam ./00_input_data/NEB_primers.fasta ./01_isoseq/lima/merged.demult.bam

# Filter for non-concatamer, polyA-containing reads
isoseq3 refine --require-polya ./01_isoseq/lima/merged.demult.NEB_5p--NEB_3p.bam ./00_input_data/NEB_primers.fasta ./01_isoseq/refine/merged.flnc.bam

# Cluster reads
isoseq3 cluster ./01_isoseq/refine/merged.flnc.bam ./01_isoseq/cluster/merged.clustered.bam --verbose --use-qvs

# Align reads to the genome 
pbmm2 align ./00_input_data/GRCh38.primary_assembly.genome.fa ./01_isoseq/cluster/merged.clustered.hq.bam ./01_isoseq/align/merged.aligned.bam --preset ISOSEQ --sort -j 40 --log-level INFO

# Collapse redundant reads
isoseq3 collapse ./01_isoseq/align/merged.aligned.bam ./01_isoseq/collapse/merged.collapsed.gff

conda deactivate
```
## Use _pbindex_ to create an index file that enables random access to PacBio-specific data in BAM files <br />
__Input file(s):__ <br />
 - raw_reads.ccs.bam <br />

## Use _bamtools_ to ensure that only qv10 reads from CCS are input <br />
__Input file(s):__ <br />
 - raw_reads.ccs.bam <br />

__Output file(s):__ 
  - filter/filtered.merged.bam <br />

## Use _lima_ to find and remove adapters & barcodes <br />
__Input file(s):__ <br />
 - primers.fasta <br />
 - filtered.merged.bam <br />

__Output file(s):__ 
  - lima/merged.demult.bam <br />

## Use _isoseq3 refine_ to filter for non-concatamer, polyA-containing reads <br \>
  __Input file(s):__ <br />
  - merged.demult.nameofprimerused.bam <br />
     - note that this is automatically labeled with your primer names <br />
  - primers.fasta <br />

__Output file(s):__ <br />
- refine/merged.flnc.bam

## Use _isoseq3 cluster_ to cluster reads <br />
__Input file(s):__ <br />
- merged.flnc.bam

__Output file(s):__ <br />
- cluster/merged.clustered.bam <br />

## Use _pbmm2 align_ (PacBio minimap2) to align reads to the genome <br />
__Inputfile(s):__ <br />
- assembly_genome.fasta <br />
- merged.clustered.hq.bam <br />

__Output file(s):__ <br />
- align/merged.aligned.bam <br />

## Use _isoseq3 collapse_ to collapse redundant reads 
__Input file(s):__ <br />
- merged.aligned.bam

__Output file(s):__ <br />
- collapse/merged.collapsed.gff

## Next go to [SQANTI module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/02_SQANTI)

