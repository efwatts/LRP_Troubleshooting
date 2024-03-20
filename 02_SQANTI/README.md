# SQANTI3 <br />
To download SQANTI3, see the [Conesa Lab Wiki](https://github.com/ConesaLab/SQANTI3/wiki/Dependencies-and-installation).

## Collapse alignments & classify transcripts <br />
_Input:_ <br />
- cDNA_Cupcake (another program needs to be in $PYTHONPATH) <br />
- merged.collapsed.gff (from Iso-Seq) <br />
- assembly_genome.fasta <br />
- merged.collapsed.abundance.txt (from Iso-Seq) <br />
- annotated_genome.gtf <br />

_Ouput:_ <br />
- corrected.fasta
- corrected.gtf
- Report with figures
- Other outpt files with information about sequence data

## To run SQANTI3
Step 1: Activate SQANTI environment <br />
```
(base)-bash-4.1$ conda activate SQANTI3.env
(SQANTI3.env)-bash-4.1$
```
Step 2: Add `cDANCupcake/sequence` to `$PYTHONPATH`
```
(SQANTI3.env)-bash-4.1$ export PYTHONPATH=$PYTHONPATH:<path_to>/cDNA_Cupcake/sequence/
(SQANTI3.env)-bash-4.1$ export PYTHONPATH=$PYTHONPATH:<path_to>/cDNA_Cupcake/
```
Step 3: Use `02_sqanti.sh` to run SQANTI3 <br />

## Next go to CPAT module
