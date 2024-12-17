#!/bin/bash

#SBATCH --job-name=SQANTI_protein
#SBATCH --cpus-per-task=10 #number of cores to use
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=12:00:00 #amount of time for the whole job
#SBATCH --partition=standard #the queue/partition to run on
#SBATCH --account=sheynkman_lab
#SBATCH --output=%x-%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=yqy3cu@virginia.edu

module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load bioconda/py3.10
module load apptainer/1.2.2
module load miniforge/24.3.0-py3.11
module load R/4.3.1 
module load perl/5.36.0 
module load star/2.7.9a 

# be sure SQANTI3 utilities are in your 00_scripts folder...I need to figure out how to fix this.
source $(conda info --base)/etc/profile.d/conda.sh
conda activate sqanti_protein

export PYTHONPATH=$PYTHONPATH:/project/sheynkman/programs/SQANTI3-5.2/cDNA_Cupcake/sequence/
export PYTHONPATH=$PYTHONPATH:/project/sheynkman/programs/SQANTI3-5.2/cDNA_Cupcake/
export PYTHONPATH=$PYTHONPATH:/project/sheynkman/programs/SQANTI3-5.2

# Mother
python 00_scripts/09_sqanti_protein.py \
mother/08_rename_cds_to_exon/Mot.transcript_exons_only.gtf \
mother/08_rename_cds_to_exon/Mot.cds_renamed_exon.gtf \
mother/05_orf_calling/Mot_best_ORF.tsv \
mother/08_rename_cds_to_exon/gencode.transcript_exons_only.gtf \
mother/08_rename_cds_to_exon/gencode.cds_renamed_exon.gtf \
-d mother/09_sqanti_protein/ \
-p Mot

conda deactivate
