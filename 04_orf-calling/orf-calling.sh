```
module load apptainer/1.2.2
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load bioconda/py3.10

apptainer pull docker://gsheynkmanlab/orf_calling:latest
```
After pulling the docker, create and activate conda environment
```
conda env create -f ./00_environments/orf_calling.yml
conda activate orf-calling
pip install gtfparse
```
Add the apptainer to the scratch folder before entering the apptainer and make sure that your working directory is in scratch so you can write output files.
```
apptainer exec --bind $SCRATCH:/project/sheynkman/users/emily/LRP_test/jurkat orf_calling_latest.sif ls /project/sheynkman/users/emily/LRP_test/jurkat
apptainer exec orf_calling_latest.sif ls $SCRATCH
```

Now enter the containter and run the script that is on Rivanna (Apptainer files are read only)
```
apptainer exec orf_calling_latest.sif /bin/bash

python ./00_scripts/04_orf_calling.py \
--orf_coord ./03_CPAT/cpat.ORF_prob.tsv \
--orf_fasta ./03_CPAT/cpat.ORF_seqs.fa \
--gencode ./00_input_data/gencode.v35.annotation.canonical.gtf \
--sample_gtf ./02_sqanti/output/jurkat_corrected.gtf \
--pb_gene ./03_transcriptome_summary/pb_gene.tsv \
--classification ./02_sqanti/output/jurkat_classification.txt \
--sample_fasta ./02_sqanti/output/jurkat_corrected.fasta \
--output ./04_orf_calling/jurkat_best_ORF.tsv
```
