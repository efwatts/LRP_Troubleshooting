# CPAT <br />
CPAT is a bioinformatics tool to predict an RNA’s coding probability based on the RNA sequence characteristics. To achieve this goal, CPAT calculates scores of sequence-based features from a set of known protein-coding genes and background set of non-coding genes. <br />

Features
- ORF size
- ORF coverage
- Fickett score
- Hexamer usage bias

CPAT will then builds a logistic regression model using these 4 features as predictor variables and the “protein-coding status” as the response variable. After evaluating the performance and determining the probability cutoff, the model can be used to predict new RNA sequences. <br />

_Input_
- Human_Hexamer.tsv
- Human_logitModel.RData
- corrected.fasta (from [02_SQANTI module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/02_SQANTI))

_Output_
- ORF_prop.tsv
- ORF_seqs.fasta

## Run CPAT
If [CPAT](https://cpat.readthedocs.io/en/latest/#introduction) isn't already installed, install CPAT and make executable. If you're on an HPC, like Rivanna, you will need to load modules first and all CPAT's install location to your `PATH`. <br />
```
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
pip install CPAT
export PATH="$HOME/.local/bin:$PATH"
```
Now you can run CPAT with the script `03_cpat.sh` on your HPC or using this command, customizing your settings and file locations:
```
cpat \
   -x ./00_input_data/Human_Hexamer.tsv \
   -d H./00_input_data/uman_logitModel.RData \
   -g ./02_sqanti/output/jurkat_corrected.fasta \
   --min-orf=50 \
   --top-orf=50 \
   -o ./03_CPAT/cpat_out \
   2> cpat.error
```

## Next go to [ORF-Calling module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/04_orf-calling)
### Note: the [Six Frame Translation module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/03_six_frame_translation) or [Transcriptome Summary module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/03_transcriptome_summary) can be done at this stage as well. 
