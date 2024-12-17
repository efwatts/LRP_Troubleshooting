# Run SUPPA to identify alternative splice sites
Run the tool from the [Computational RNA Biology group](https://github.com/comprna), [SUPPA](https://github.com/comprna/SUPPA). <br />

If using an HPC, like Rivanna at UVA, load your modules. Activate conda environment. 
```
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load miniforge/24.3.0-py3.11
module load R/4.4.1

conda activate suppa
```
Generate splicing events. 
```
python /project/sheynkman/programs/SUPPA-2.4/suppa.py generateEvents -i /project/sheynkman/external_data/GENCODE_M35/gencode.vM35.basic.annotation.gtf -o SUPPA/events -f ioi

python /project/sheynkman/programs/SUPPA-2.4/suppa.py generateEvents -i 08_rename_cds_to_exon/WT/WT.cds_renamed_exon.gtf -o 18_SUPPA/LRP_events/WT.events -e SE SS MX RI FL -f ioe
python /project/sheynkman/programs/SUPPA-2.4/suppa.py generateEvents -i 08_rename_cds_to_exon/Q157R/Q157R.cds_renamed_exon.gtf -o 18_SUPPA/LRP_events/Q157R.events -e SE SS MX RI FL -f ioe
```
Put all IOE events in the same file.
```
cd 18_SUPPA/LRP_events/

awk '
    FNR==1 && NR!=1 { while (/^<header>/) getline; }
    1 {print}
' *.ioe > all.LRP.events.ioe

cd ../..
```
Create expression table.
```
python 00_scripts/18_suppa_expression_table.py -f 17_track_visualization/WT/WT_refined_cds.bed12 17_track_visualization/Q157R/Q157R_refined_cds.bed12 -s sample1 sample2 -o 18_SUPPA/combined.cpm
```
Calculate PSI values.
```
python /project/sheynkman/programs/SUPPA-2.4/suppa.py psiPerEvent --ioe-file 18_SUPPA/LRP_events/all.LRP.events.ioe --expression-file 18_SUPPA/combined.cpm -o 18_SUPPA/combined_local
```
Differential splicing. Split the PSI and TPM files between the two conditions (if comparing).
```
Rscript 00_scripts/split_file.R 18_SUPPA/combined.cpm sample1 sample2 18_SUPPA/WT_sample1.tpm 18_SUPPA/Q157R_sample2.tpm -i
Rscript 00_scripts/split_file.R 18_SUPPA/combined_local.psi sample1 sample2 18_SUPPA/WT_sample1.psi 18_SUPPA/Q157R_sample2.psi -e
```
Analyze differential splicing.
```
python /project/sheynkman/programs/SUPPA-2.4/suppa.py diffSplice \
    -m empirical \
    -i 18_SUPPA/LRP_events/all.LRP.events.ioe \
    -p 18_SUPPA/WT_sample1.psi 18_SUPPA/Q157R_sample2.psi \
    -e 18_SUPPA/WT_sample1.tpm 18_SUPPA/Q157R_sample2.tpm \
    -gc \
    -o 18_SUPPA/diff_splice_events

conda deactivate
module purge
```
