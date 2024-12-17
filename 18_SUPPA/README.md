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
