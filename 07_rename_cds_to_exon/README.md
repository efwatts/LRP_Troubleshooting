# Rename CDS to exon
Make GTF input files for the next module, sqanti protein. These are basically making CDS regions look like exons. <br />

_Input:_ <br />
- cds.gtf (from [06_make_cds_gtf module](https://github.com/efwatts/LRP_Troubleshooting/blob/main/06_make_cds_gtf/README.md))
- reference.gtf (from [Gencode](https://www.gencodegenes.org/), also used in [01_reference_tables module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_reference_tables))

_Output:_
- gencode.cds_renamed_exon.gtf
- gencode.transcript_exons_only.gtf
- jurkat.cds_renamed_exon.gtf
- jurkat.transcript_exons_only.gtf

## Run rename CDS to exon
I had to run this one in a container as well, and I ran it in the reference tables environment (kind of by accident, but it worked). Load modules (if using Rivanna or other HPC), load the [reference tables environment](https://github.com/efwatts/LRP_Troubleshooting/blob/main/01_reference_tables/reference_tables.yml), and download the container. <br />
```
module load apptainer/1.2.2
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load bioconda/py3.10

conda activate reference_tab
```
Then enter the apptainer and call the python script either using `07_rename_cds_to_exon.sh` or the following command: <br />
```
apptainer exec pb-cds-gtf_latest.sif /bin/bash

python ./00_scripts/07_rename_cds_to_exon.py \
--sample_gtf ./06_make_cds_gtf/jurkat_cds.gtf \
--sample_name ./07_rename_cds_to_exon/jurkat \
--reference_gtf ./00_input_data/gencode.v35.annotation.canonical.gtf \
--reference_name ./07_rename_cds_to_exon/gencode 

exit

conda deactivate 
```
