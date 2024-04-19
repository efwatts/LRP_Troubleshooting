# Make CDS GTF
Make a GTF file with coding sequences...mapping to the genome where coding information is held.<br />
*Note, some of the input naming is a little confusing...I'll likely modify this in later iterations of the LRP.*<br />
....fun update--the cds.gtf file is blank 4/19/24 <br/>

_Input:_ <br />
- corrected.gtf (from [SQANT module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/02_SQANTI))
- orf_refined.tsv (from [Refine ORF Database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/05_refine_orf_database)) 
- best_ORF.tsv (from [ORF-calling module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/04_orf-calling))
- pb_gene.tsv (from [Transcriptome Summary module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/03_transcriptome_summary))

_Output:_
- cds.gtf

## Run ORF calling
I had to run this one in a container as well. Load modules (if using Rivanna or other HPC), load the [reference tables environment](https://github.com/efwatts/LRP_Troubleshooting/blob/main/01_reference_tables/reference_tables.yml), and download the container. <br />
```
module load apptainer/1.2.2
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load bioconda/py3.10

apptainer pull docker://gsheynkmanlab/pb-cds-gtf:latest

conda activate reference_tab
```
Add the apptainer to the scratch folder before entering the apptainer and make sure that your working directory is in scratch so you can write output files.
```
apptainer exec --bind $SCRATCH:/project/sheynkman/users/emily/LRP_test/jurkat pb-cds-gtf_latest.sif ls /project/sheynkman/users/emily/LRP_test/jurkat
apptainer exec pb-cds-gtf_latest.sif ls $SCRATCH
```
Then enter the apptainer and call the python script either using `06_make_pacbio_cds_gtf.sh` or the following command: <br />
```
apptainer exec pb-cds-gtf_latest.sif /bin/bash

python ./00_scripts/06_make_pacbio_cds_gtf.py \
--sample_gtf ./02_sqanti/output/jurkat_corrected.gtf \
--agg_orfs ./05_refine_orf_database/jurkat_30_orf_refined.tsv \
--refined_orfs ./04_orf_calling/jurkat_best_ORF.tsv \
--pb_gene ./03_transcriptome_summary/pb_gene.tsv \
--output_cds ./06_make_cds_gtf/jurkat_cds.gtf

exit

conda deactivate 
```
