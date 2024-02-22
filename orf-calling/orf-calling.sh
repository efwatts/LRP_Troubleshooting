##trying on Rivanna
module load apptainer/1.2.2
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load bioconda/py3.10

#I activated already built conda env....not sure if this is a good idea
#orf-calling is already an env on Rivanna for me, so it wouldn't let me build a new one
#if this doesn't work, delete that env and build new from container 
conda activate orf-calling 

##BE SURE TO DO THIS BEFORE OPENING THE APPTAINER SO YOU CAN WRITE OUTPUT FILES
apptainer exec --bind $SCRATCH:/scratch/yqy3cu/ORF_docker tutorial.sif ls /scratch

#now be sure your working directory on Rivanna is in your scratch...otherwise you won't be able to write output files
apptainer exec orf_calling_latest.sif ls $SCRATCH

#now enter the containter 
apptainer exec orf_calling_latest.sif /bin/bash

#run script that is on Rivanna (APPTAINER FILES ARE READ ONLY)
python /scratch/yqy3cu/ORF_docker/orf_calling.py \
--orf_coord /scratch/yqy3cu/ORF_docker/jurkat_chr22.ORF_prob.tsv \
--orf_fasta /scratch/yqy3cu/ORF_docker/jurkat_chr22.ORF_seqs.fa \
--gencode /scratch/yqy3cu/ORF_docker/gencode.v35.annotation.chr22.gtf \
--sample_gtf /scratch/yqy3cu/ORF_docker/jurkat_chr22_corrected.gtf \
--pb_gene /scratch/yqy3cu/ORF_docker/pb_gene.tsv \
--classification /scratch/yqy3cu/ORF_docker/jurkat_chr22_classification.txt \
--sample_fasta /scratch/yqy3cu/ORF_docker/jurkat_chr22_corrected.fasta \
--output /scratch/yqy3cu/ORF_docker/jurkat_cpat.ORF_called.tsv
