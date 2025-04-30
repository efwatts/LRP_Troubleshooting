# SQANTI3 <br />
This module corrects any errors in alignment from IsoSeq3 and classifies each accession in relation to the reference genome. <br />

To download SQANTI3, see the [Conesa Lab Wiki](https://github.com/ConesaLab/SQANTI3/wiki/Dependencies-and-installation).
You may have to change line 25 in `setup.py` from the SQANTI3-5.2 downlod from `ext_modules = cythonize(ext_modules),` to `ext_modules = cythonize(ext_modules, language_level = "2"),` <br />
You may also have to change any instances of `mean` to `np.mean` and stop calling `scipy`, becuase the `mean` function in `scipy` is degraded. <br />
Here is an AI generated summary of this step: <br />
> The `sqanti3_qc.py` script is designed to perform quality control and classification of long-read RNA-seq data. It takes as input a GFF file containing transcript annotations, a GTF file with gene annotations, and a FASTA file with genome sequences. The script generates several output files, including a summary report, a classification report, and various QC metrics. The classification report categorizes transcripts into different classes based on their alignment to the reference genome and their relationship to known genes. The QC metrics provide information on the quality of the input data and the performance of the classification process.
## Input files <br />
- `merged.collapsed.gff` - GFF file from IsoSeq3 <br />
- `gencode.v47.basic.annotation.gtf` - GTF file from [Gencode](https://www.gencodegenes.org/) <br />
- `GRCh38.primary_assembly.genome.fa` - Genome fasta file from [Gencode](https://www.gencodegenes.org/) <br />
- `merged.collapsed.flnc_count.txt` - Flnc count file from IsoSeq3 <br />

## Required installations: <br />
If you are in the Sheynkman Lab, SQANTI3 is already downloadable and executable on Rivanna is `/project/sheynkman/programs/SQANTI3-5.2` <br />

SQANTI3: <br />
```
wget https://github.com/ConesaLab/SQANTI3/archive/refs/tags/v5.2.tar.gz
tar -xvf v5.2.tar.gz
cd SQANTI3-5.2
conda env create -f SQANTI3.conda_env.yml
conda activate SQANTI3.env
```
Load module (if on HPC) and create and activate conda environment. <br />
```
module load gcc/11.4.0
module load openmpi/4.1.4
module load R/4.3.1 
module load python/3.11.4 
module load miniforge/24.3.0-py3.11
module load perl/5.36.0 
module load star/2.7.9a 
module load kallisto/0.48.0

conda env create -f 00_environments/SQANTI3_env.yml
conda activate SQANTI3.env
```

## Run SQANTI3 from a SLURM script <br />
```
sbatch 00_scripts/02_sqanti.sh
```
## Or run these commands. <br />
Note: you have to add SQANTI3 cDNA_Cupcake directory to your path. <br />
```
chmod +x /project/sheynkman/programs/SQANTI3-5.2/utilities/gtfToGenePred
export PYTHONPATH=$PYTHONPATH:/project/sheynkman/programs/SQANTI3-5.2/cDNA_Cupcake/sequence/
export PYTHONPATH=$PYTHONPATH:/project/sheynkman/programs/SQANTI3-5.2/cDNA_Cupcake/

python /project/sheynkman/programs/SQANTI3-5.2/sqanti3_qc.py \
    -o sample \
    -d 02_sqanti \
    --skipORF \
    --fl_count 01_isoseq/collapse/merged.collapsed.flnc_count.txt \
    01_isoseq/collapse/merged.collapsed.gff \
    /project/sheynkman/external_data/GENCODE_v47/gencode.v47.basic.annotation.gtf \
    /project/sheynkman/external_data/GENCODE_v47/GRCh38.primary_assembly.genome.fa

conda deactivate
module purge
```

## Next go to [Filter SQANTI module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/03_filter_sqanti)
### Note: the [Make Gencode Database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/02_make_gencode_database) can be done at this stage as well. 
