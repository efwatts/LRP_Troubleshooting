#!/bin/bash

#SBATCH --job-name=18_suppa_rmats_compare
#SBATCH --cpus-per-task=10 #number of cores to use
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=24:00:00 #amount of time for the whole job
#SBATCH --partition=standard #the queue/partition to run on
#SBATCH --account=sheynkman_lab
#SBATCH --output=log_files/%x-%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=yqy3cu@virginia.edu

module load gcc
module load openmpi
module load python
module load miniforge
module load R
module load perl

conda activate suppa

# Step 1: Clean CSV to TSV and remove quotes
cat 18_SUPPA/rMATS_data/SpliceEventsQ157Rwithexons.csv \
  | sed 's/"//g' \
  | tr ',' '\t' \
  > 18_SUPPA/rMATS_data/rmats_cleaned.tsv

# Step 2: Extract event types ("se", "a3", "a5") and restrict to required columns 1–14
awk -F'\t' 'NR==1 || ($1=="se" && $2!="" && $14!="") { for(i=1;i<=14;i++) printf $i (i<14? "\t" : "\n") }' \
  18_SUPPA/rMATS_data/rmats_cleaned.tsv > 18_SUPPA/rMATS_data/SE_events.txt

awk -F'\t' 'NR==1 || ($1=="a3" && $2!="" && $14!="") { for(i=1;i<=14;i++) printf $i (i<14? "\t" : "\n") }' \
  18_SUPPA/rMATS_data/rmats_cleaned.tsv > 18_SUPPA/rMATS_data/A3_events.txt

awk -F'\t' 'NR==1 || ($1=="a5" && $2!="" && $14!="") { for(i=1;i<=14;i++) printf $i (i<14? "\t" : "\n") }' \
  18_SUPPA/rMATS_data/rmats_cleaned.tsv > 18_SUPPA/rMATS_data/A5_events.txt

# Step 3: Run conversion scripts
perl /project/sheynkman/programs/SUPPA-2.4/rmats_to_suppa_ids_SE_events.pl 18_SUPPA/rMATS_data/SE_events.txt > 18_SUPPA/rMATS_data/SE.rMATS.toSUPPA.txt
perl /project/sheynkman/programs/SUPPA-2.4/rmats_to_suppa_ids_A3_events.pl 18_SUPPA/rMATS_data/A3_events.txt > 18_SUPPA/rMATS_data/A3.rMATS.toSUPPA.txt
perl /project/sheynkman/programs/SUPPA-2.4/rmats_to_suppa_ids_A5_events.pl 18_SUPPA/rMATS_data/A5_events.txt > 18_SUPPA/rMATS_data/A5.rMATS.toSUPPA.txt

# Step 4: Tag event types for merging
awk '{print $0 "\tSE"}' 18_SUPPA/rMATS_data/SE.rMATS.toSUPPA.txt > 18_SUPPA/rMATS_data/SE.labeled.txt
awk '{print $0 "\tA3"}' 18_SUPPA/rMATS_data/A3.rMATS.toSUPPA.txt > 18_SUPPA/rMATS_data/A3.labeled.txt
awk '{print $0 "\tA5"}' 18_SUPPA/rMATS_data/A5.rMATS.toSUPPA.txt > 18_SUPPA/rMATS_data/A5.labeled.txt

# Step 5: Merge all into a single table
cat 18_SUPPA/rMATS_data/SE.labeled.txt 18_SUPPA/rMATS_data/A3.labeled.txt 18_SUPPA/rMATS_data/A5.labeled.txt \
  > 18_SUPPA/rMATS_data/rMATS_all_events_SUPPA_IDs.tsv

# Step 6: give the output a header
(echo -e "Event_ID\tGene\trMATS_dPSI\trMATS_FDR\tEvent_Type"; cat 18_SUPPA/rMATS_data/rMATS_all_events_SUPPA_IDs.tsv) \
> 18_SUPPA/rMATS_data/rMATS_all_events_SUPPA_IDs_labeled.tsv

# Step 7: Merge and visualize in R
Rscript 00_scripts/18_suppa_rmats_merge.R