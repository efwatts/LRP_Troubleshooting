# Iso-Seq 

## Required installations:
The bioconda library 'isoseq3' can be installed via `conda install bioconda::isoseq3` 

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

## Next go to SQANTI module

