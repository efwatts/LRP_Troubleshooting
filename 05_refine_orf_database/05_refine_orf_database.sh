module load apptainer/1.2.2
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load bioconda/py3.10

conda env create -f ./00_environments/refine_orf_database.yml
conda activate refined-database-generation

python ./00_scripts/05_refine_orf_database.py \
--name ./05_refine_orf_database/jurkat_30 \
--orfs ./04_orf_calling/jurkat_best_ORF.tsv \
--pb_fasta ./02_sqanti/output/jurkat_corrected.fasta \
--coding_score_cutoff 0.3 

conda deactivate 

