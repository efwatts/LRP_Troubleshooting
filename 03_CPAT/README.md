# CPAT <br />
Predicts coding probability of transcripts <br />
_Input_
- Human_Hexamer.tsv
- Human_logitModel.RData
- corrected.fasta (from SQANTI3)

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
## Next go to orf-calling module
