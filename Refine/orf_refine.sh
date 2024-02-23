conda env create -f environment.yml
conda activate refined-database-generation

python refine_orf_database.py \
--name jurkat_30 \
--orfs ../jurkat_cpat.ORF_called.tsv \
--pb_fasta ../jurkat_chr22_corrected.fasta
