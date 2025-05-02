# CPAT <br />
CPAT is a bioinformatics tool to predict an RNA’s coding probability based on the RNA sequence characteristics. To achieve this goal, CPAT calculates scores of sequence-based features from a set of known protein-coding genes and background set of non-coding genes. <br />

Features
- ORF size
- ORF coverage
- Fickett score
- Hexamer usage bias

CPAT will then builds a logistic regression model using these 4 features as predictor variables and the “protein-coding status” as the response variable. After evaluating the performance and determining the probability cutoff, the model can be used to predict new RNA sequences. <br />

Here is an AI generated summary of this step: <br />
> The `cpat` tool is designed to predict the coding potential of RNA sequences using a logistic regression model. It takes as input a hexamer file, a logit model file, and a FASTA file containing RNA sequences. The script calculates various features for each RNA sequence, including ORF size, ORF coverage, Fickett score, and hexamer usage bias. It then applies the logistic regression model to predict the coding potential of the RNA sequences and generates output files with the predictions and associated features.

## Input files
- `Human_Hexamer.tsv` - Hexamer file from CPAT
- `Human_logitModel.RData` - Logit model file from CPAT
- `corrected.5degfilter.fasta` - SQANTI3 corrected FASTA file from [03_filter_sqanti module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/03_filter_sqanti)

## Required installations
If [CPAT](https://cpat.readthedocs.io/en/latest/#introduction) isn't already installed, install CPAT and make executable. If you're on an HPC, like Rivanna, you will need to load modules first and all CPAT's install location to your `PATH`. <br />
```
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load R/4.3.1
module load miniforge/24.3.0-py3.11

pip install CPAT
export PATH="$HOME/.local/bin:$PATH"
```
## Run CPAT from a SLURM script
```
sbatch 00_scripts/04_cpat.sh
```
## Or run these commands.
```
cpat \
   -x /project/sheynkman/external_data/CPAT_data/Human_Hexamer.tsv \
   -d /project/sheynkman/external_data/CPAT_data/Human_logitModel.RData \
   -g 03_filter_sqanti/sample_corrected.5degfilter.fasta \
   --min-orf=50 \
   --top-orf=50 \
   -o 04_CPAT/sample \
   2> 04_CPAT/sample_cpat.error

python 00_scripts/04_filter_cpat_results.py \
  --cpat_output 04_CPAT/sample.ORF_prob.tsv \
  --input_fasta 03_filter_sqanti/sample_corrected.5degfilter.fasta \
  --output_dir 04_CPAT/dropout \
  --prefix sample

conda deactivate
module purge
```

## Next go to [05_orf-calling module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/05_orf-calling)
### Note: the [04_transcriptome_summary module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/04_transcriptome_summary) can be done at this stage as well. 
