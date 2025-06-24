#!/bin/bash

#SBATCH --job-name=09_sqanti_protein
#SBATCH --cpus-per-task=10 #number of cores to use
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=12:00:00 #amount of time for the whole job
#SBATCH --partition=standard #the queue/partition to run on
#SBATCH --account=your_account_name #the account to charge the job to
#SBATCH --output=log_files/%x-%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=your_email #your email address to receive notifications

module load gcc
module load openmpi
module load python
module load apptainer
module load miniforge
module load R
module load perl
module load star

# be sure SQANTI3 utilities are in your 00_scripts folder...I have not yet found a way around this.

conda activate sqanti_protein

export PYTHONPATH=$PYTHONPATH:/project/sheynkman/programs/SQANTI3-5.2/cDNA_Cupcake/sequence/
export PYTHONPATH=$PYTHONPATH:/project/sheynkman/programs/SQANTI3-5.2/cDNA_Cupcake/
export PYTHONPATH=$PYTHONPATH:/project/sheynkman/programs/SQANTI3-5.2

# condition 1
python 00_scripts/09_sqanti_protein.py \
08_rename_cds_to_exon/condition1.transcript_exons_only.gtf \
08_rename_cds_to_exon/condition1.cds_renamed_exon.gtf \
05_orf_calling/best_ORF_condition1.tsv \
08_rename_cds_to_exon/gencode.transcript_exons_only.gtf \
08_rename_cds_to_exon/gencode.cds_renamed_exon.gtf \
-d 09_sqanti_protein/ \
-p condition1

# condition 2
python 00_scripts/09_sqanti_protein.py \
08_rename_cds_to_exon/condition2.transcript_exons_only.gtf \
08_rename_cds_to_exon/condition2.cds_renamed_exon.gtf \
05_orf_calling/best_ORF_condition2.tsv \
08_rename_cds_to_exon/gencode.transcript_exons_only.gtf \
08_rename_cds_to_exon/gencode.cds_renamed_exon.gtf \
-d 09_sqanti_protein/ \
-p condition2

conda deactivate
module purge