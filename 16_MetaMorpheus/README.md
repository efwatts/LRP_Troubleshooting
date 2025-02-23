# MetaMorpheus
Use the proteomics search software, [MetaMorpheus](https://github.com/smith-chem-wisc/MetaMorpheus).
_Input:_ <br />
- .toml file with configuration parameters (example included in this module_
- .mzML file(s) from [15_MS_file_convert module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/15_MS_file_convert)
- database.fasta file from [02_make_gencode_database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/02_make_gencode_database) or [14_make_hybrid_database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/14_make_hybrid_database)
  
_Output:_
- AllPeptides.psmtsv
- AllQuantifiedPeaks.tsv
- AutoGeneratedManuscriptProse.txt
- results.txt
- AllPSMs_FormattedForPercolator.tab
- AllQuantifiedPeptides.tsv
- 'Individual File Results' folder
- AllPSMs.psmtsv
- AllQuantifiedProteinGroups.tsv
- model.zip

## Run script
If running on Rivanna or other HPC, load required modules. Create, load, and populate environment. 
```
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load bioconda/py3.10
module load miniforge/24.3.0-py3.11

conda create -n metamorph
conda activate metamorph
conda install -c conda-forge metamorpheus
```
Call the slurm script if on HPC. 
```
sbatch ./00_scripts/16_metamorpheus.sh
```
Or run these commands from the command line. 
```
conda activate metamorph

#gencode only
metamorpheus -t ./00_input_data/Task1SearchTaskconfig_orf.toml \
-s ./15_MS_file_convert/120426_Jurkat_highLC_Frac1.mzML ./15_MS_file_convert/120426_Jurkat_highLC_Frac2.mzML ./15_MS_file_convert/120426_Jurkat_highLC_Frac3.mzML ./15_MS_file_convert/120426_Jurkat_highLC_Frac4.mzML ./15_MS_file_convert/120426_Jurkat_highLC_Frac5.mzML ./15_MS_file_convert/120426_Jurkat_highLC_Frac6.mzML ./15_MS_file_convert/120426_Jurkat_highLC_Frac7.mzML ./15_MS_file_convert/120426_Jurkat_highLC_Frac8.mzML ./15_MS_file_convert/120426_Jurkat_highLC_Frac9.mzML ./15_MS_file_convert/120426_Jurkat_highLC_Frac10.mzML \
-d ./02_make_gencode_database/gencode_clusters.fasta \
-o ./16_MetaMorpheus/gencode/

#hybrid database
metamorpheus -t ./00_input_data/Task1SearchTaskconfig_orf.toml \
-s ./15_MS_file_convert/120426_Jurkat_highLC_Frac1.mzML ./15_MS_file_convert/120426_Jurkat_highLC_Frac2.mzML ./15_MS_file_convert/120426_Jurkat_highLC_Frac3.mzML ./15_MS_file_convert/120426_Jurkat_highLC_Frac4.mzML ./15_MS_file_convert/120426_Jurkat_highLC_Frac5.mzML ./15_MS_file_convert/120426_Jurkat_highLC_Frac6.mzML ./15_MS_file_convert/120426_Jurkat_highLC_Frac7.mzML ./15_MS_file_convert/120426_Jurkat_highLC_Frac8.mzML ./15_MS_file_convert/120426_Jurkat_highLC_Frac9.mzML ./15_MS_file_convert/120426_Jurkat_highLC_Frac10.mzML \
-d ./13_protein_hybrid_database/jurkat_hybrid.fasta \
-o ./16_MetaMorpheus/hybrid/

conda deactivate
```
**note:** *I want to modify this file structure so that more runs can happen seamlessly. I also want to better automate it.*

## Proceed to
