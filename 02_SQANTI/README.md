# SQANTI3 <br />
Corrects any errors in alignment from IsoSeq3 and classifies each accession in relation to the reference genome. <br />

To download SQANTI3, see the [Conesa Lab Wiki](https://github.com/ConesaLab/SQANTI3/wiki/Dependencies-and-installation).
You may have to change line 25 in `setup.py` from the SQANTI3-5.2 downlod from `ext_modules = cythonize(ext_modules),` to `ext_modules = cythonize(ext_modules, language_level = "2"),` <br />
You may also have to change any instances of `mean` to `np.mean` and stop calling `scipy`, becuase the `mean` function in `scipy` is degraded. <br />
```
wget https://github.com/ConesaLab/SQANTI3/archive/refs/tags/v5.2.tar.gz
tar -xvf v5.2.tar.gz
cd SQANTI3-5.2
conda env create -f SQANTI3.conda_env.yml
conda activate SQANTI3.env

git clone https://github.com/Magdoll/cDNA_Cupcake.git
cd cDNA_Cupcake
python setup.py build
python setup.py install
```

## Collapse alignments & classify transcripts <br />
_Input:_ <br />
- cDNA_Cupcake (another program needs to be in $PYTHONPATH) <br />
- merged.collapsed.gff (from [01_Iso-Seq module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_Iso-Seq)) <br />
- assembly_genome.fasta <br />
- merged.collapsed.abundance.txt (from [01_Iso-Seq module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_Iso-Seq)) <br />
- annotated_genome.gtf (from [Gencode](https://www.gencodegenes.org/)) <br />

_Ouput:_ <br />
- corrected.fasta
- corrected.gtf
- Report with figures
- Other outpt files with information about sequence data

## To run SQANTI3
Step 1: Activate SQANTI environment and set working directory. <br />
```
conda activate SQANTI3.env
cd /project/sheynkman/users/emily/LRP_test/jurkat
```
Step 2: Add `cDANCupcake/sequence` to `$PYTHONPATH` and give `gtfToGenePred` appropriate permissions. <br />
```
chmod +x ./02_sqanti/SQANTI3-5.2/utilities/gtfToGenePred
export PYTHONPATH=$PYTHONPATH:./02_sqanti/SQANTI3-5.2/cDNA_Cupcake/sequence/
export PYTHONPATH=$PYTHONPATH:./02_sqanti/SQANTI3-5.2/cDNA_Cupcake/
```
Step 3: Use `02_sqanti.sh` to run SQANTI3 if running on Rivanna or other HPC. Otherwise, run this code (changing your file locations appropriately) <br />
```
python ./02_sqanti/SQANTI3-5.2/sqanti3_qc.py \
./01_isoseq/collapse/merged.collapsed.gff \
./00_input_data/gencode.v35.annotation.canonical.gtf \
./00_input_data/GRCh38.primary_assembly.genome.fa \
--skipORF \
-o jurkat \
-d ./02_sqanti/output/ \
--fl_count ./01_isoseq/collapse/merged.collapsed.abundance.txt
```

## To filter SQANTI3 results
...

## Next go to [CPAT module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/03_CPAT), [Six Frame Translation module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/03_six_frame_translation), or [Transcriptome Summary module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/03_transcriptome_summary)
### Note: the [Make Gencode Database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/02_make_gencode_database) can be done at this stage as well. 
