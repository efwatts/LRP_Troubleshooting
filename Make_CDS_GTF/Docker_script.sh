ocker pull gsheynkmanlab/pb-cds-gtf

docker run -it --rm gsheynkmanlab/pb-cds-gtf /bin/bash

conda env create -f environment.yml

#run on other terminal  
docker cp ./cds_gtf_files sleepy_yalow:/

cd cds_gtf_files

conda activate reference-tables
conda install bioconda::gtfparse

python make_pacbio_cds_gtf.py \
--sample_gtf merged.collapsed.gff \
--agg_orfs jurkat_30_orf_refined.tsv \
--refined_orfs jurkat_cpat.ORF_called.tsv \
--pb_gene pb_gene.tsv \
--output_cds toy_cds.gtf


#run on other terminal 
docker cp upbeat_cori:/cds_gtf_files/toy_cds.gtf /Users/emilywatts/Desktop
#oh no! The file is empty 
