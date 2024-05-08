# Sqanti Protein
This is a [method previously developed by our group](https://github.com/sheynkman-lab/Long-Read-Proteogenomics/tree/main/modules/sqanti_protein) designed to classify the proteins found by the LRP using the [SQANTI3](https://github.com/ConesaLab/SQANTI3) naming conventions. It is an adaptation of the SQANTI3 script `sqanti3_qc.py`. <br />

_Input:_ <br />
- gencode.cds_renamed_exon.gtf (from [Rename CDS to exon module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/07_rename_cds_to_exon))
- gencode.transcript_exons_only.gtf (from [Rename CDS to exon module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/07_rename_cds_to_exon))
- best_ORF.tsv (from [ORF-calling module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/04_orf-calling))
- jurkat.cds_renamed_exon.gtf (from [Rename CDS to exon module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/07_rename_cds_to_exon))
- jurkat.transcript_exons_only.gtf (from [Rename CDS to exon module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/07_rename_cds_to_exon))
  
_Output:_
- sqanti_protein_classification.tsv
- refAnnotation.genePred

## Run sqanti_protein
If running on Rivanna or other HPC, load required modules.
```
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load bioconda/py3.10
module load apptainer/1.2.2
module load anaconda/2023.07-py3.11
module load R/4.3.1 
module load perl/5.36.0 
module load star/2.7.9a 
```
I'm going to create a new conda environment, because conda keeps saying that loaded packages aren't actually loaded. <br />
The log of rest of the packages I loaded were lost in a saving error...but the script will tell you which modules it is missing!
```
conda create -n sqanti_protein

conda activate sqanti_protein
conda install argparse
pip install bx-python
```
Add sqanti scripts, cDNACupckae to $PYTHONPATH and activate environment (if environment is already created)
```
export PYTHONPATH=/project/sheynkman/users/emily/LRP_test/jurkat/02_sqanti/SQANTI3-5.2:$PYTHONPATH
export PYTHONPATH=/project/sheynkman/users/emily/LRP_test/jurkat/02_sqanti/SQANTI3-5.2/cDNA_Cupcake:$PYTHONPATH
export PYTHONPATH=/project/sheynkman/users/emily/LRP_test/jurkat/02_sqanti/SQANTI3-5.2/cDNA_Cupcake/sequence:$PYTHONPATH

conda activate sqanti_protein
```
Run sqanti_protein
```
python ./00_scripts/08_sqanti_protein.py \
./07_rename_cds_to_exon/jurkat.transcript_exons_only.gtf \
./07_rename_cds_to_exon/jurkat.cds_renamed_exon.gtf \
./04_orf_calling/jurkat_best_ORF.tsv \
./07_rename_cds_to_exon/gencode.transcript_exons_only.gtf \
./07_rename_cds_to_exon/gencode.cds_renamed_exon.gtf \
-d ./08_sqanti_protein/ \
-p jurkat

conda deactivate
```

## Proceed to [5 Prime UTR module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/09_5p_utr)
