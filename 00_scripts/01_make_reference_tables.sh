#!/bin/bash

#SBATCH --job-name=01_reference_tab
#SBATCH --cpus-per-task=10 #number of cores to use
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=12:00:00 #amount of time for the whole job
#SBATCH --partition=standard #the queue/partition to run on
#SBATCH --account=your_account_name #the account to charge the job to
#SBATCH --output=log_files/%x-%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=your_email #your email address to receive notifications

# Load necessary modules (if needed)
module purge
module load isoseqenv
module load apptainer
module load gcc
module load bedops
module load nseg
module load openmpi
module load python
module load miniforge

source $(conda info --base)/etc/profile.d/conda.sh

conda activate reference_tab

apptainer exec /project/sheynkman/dockers/LRP/generate-reference-tables_latest.sif /bin/bash -c "\
    python 00_scripts/01_prepare_reference_tables.py \
        --gtf /project/sheynkman/external_data/GENCODE_v47/gencode.v47.basic.annotation.gtf \
        --fa /project/sheynkman/external_data/GENCODE_v47/gencode.v47.pc_transcripts.fa \
        --ensg_gene 01_reference_tables/ensg_gene.tsv \
        --enst_isoname 01_reference_tables/enst_isoname.tsv \
        --gene_ensp 01_reference_tables/gene_ensp.tsv \
        --gene_isoname 01_reference_tables/gene_isoname.tsv \
        --isoname_lens 01_reference_tables/isoname_lens.tsv \
        --gene_lens 01_reference_tables/gene_lens.tsv \
        --protein_coding_genes 01_reference_tables/protein_coding_genes.txt
"
exit
conda deactivate
