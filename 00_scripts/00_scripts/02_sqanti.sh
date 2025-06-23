#!/bin/bash

#SBATCH --job-name=02_sqanti
#SBATCH --cpus-per-task=10 #number of cores to use
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=12:00:00 #amount of time for the whole job
#SBATCH --partition=standard #the queue/partition to run on
#SBATCH --account=sheynkman_lab
#SBATCH --output=log_files/%x-%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=yqy3cu@virginia.edu

module load gcc
module load openmpi
module load R 
module load python
module load miniforge
module load perl
module load star 
module load kallisto

source $(conda info --base)/etc/profile.d/conda.sh

conda activate SQANTI3.env

chmod +x /project/sheynkman/programs/SQANTI3-5.2/utilities/gtfToGenePred
export PYTHONPATH=$PYTHONPATH:/project/sheynkman/programs/SQANTI3-5.2/cDNA_Cupcake/sequence/
export PYTHONPATH=$PYTHONPATH:/project/sheynkman/programs/SQANTI3-5.2/cDNA_Cupcake/

python /project/sheynkman/programs/SQANTI3-5.2/sqanti3_qc.py \
    -o MDS \
    -d 02_sqanti \
    --skipORF \
    --fl_count 01_isoseq/collapse/merged.0.50.100.collapsed.flnc_count.txt \
    01_isoseq/collapse/merged.0.50.100.collapsed.gff \
    /project/sheynkman/external_data/GENCODE_M35/gencode.vM35.basic.annotation.gtf \
    /project/sheynkman/external_data/GENCODE_M35/GRCm39.primary_assembly.genome.fa

conda deactivate
module purge