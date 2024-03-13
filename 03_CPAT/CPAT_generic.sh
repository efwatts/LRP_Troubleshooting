cpat \
   -x Human_Hexamer.tsv \
   -d Human_logitModel.RData \
   -g corrected.fasta \
   --min-orf=50 \
   --top-orf=50 \
   -o cpat_out_dir \
   2> cpat.error
