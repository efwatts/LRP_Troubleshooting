# Sqanti Protein
This is a [method previously developed by our group](https://github.com/sheynkman-lab/Long-Read-Proteogenomics/tree/main/modules/sqanti_protein) designed to classify the proteins found by the LRP using the [SQANTI3](https://github.com/ConesaLab/SQANTI3) naming conventions. It is an adaptation of the SQANTI3 script `sqanti3_qc.py`. <br />

_Input:_ <br />
- gencode.cds_renamed_exon.gtf (from [08 Rename CDS to exon module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/08_rename_cds_to_exon))
- gencode.transcript_exons_only.gtf (from [08 Rename CDS to exon module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/08_rename_cds_to_exon))
- best_ORF.tsv (from [05 ORF-calling module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/05_orf-calling))
- jurkat.cds_renamed_exon.gtf (from [08 Rename CDS to exon module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/08_rename_cds_to_exon))
- jurkat.transcript_exons_only.gtf (from [08 Rename CDS to exon module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/08_rename_cds_to_exon))
  
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
module load miniforge/24.3.0-py3.11
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
python ./00_scripts/09_sqanti_protein.py \
./08_rename_cds_to_exon/jurkat.transcript_exons_only.gtf \
./08_rename_cds_to_exon/jurkat.cds_renamed_exon.gtf \
./05_orf_calling/jurkat_best_ORF.tsv \
./08_rename_cds_to_exon/gencode.transcript_exons_only.gtf \
./08_rename_cds_to_exon/gencode.cds_renamed_exon.gtf \
-d ./09_sqanti_protein/ \
-p jurkat

conda deactivate
```

## Proceed to [10_5p_utr module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/10_5p_utr)
