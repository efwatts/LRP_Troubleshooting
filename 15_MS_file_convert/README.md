# Mass Spectrometry File Conversion 
Convert .raw MS files to .mzML files for downstream analysis using [msconvert](https://proteowizard.sourceforge.io/tools/msconvert.html). For Mac and HPC, I used [this tutorial](https://github.com/Jiung-Wen/msdial) to figure out how to run msconvert.

_Input:_ <br />
- .raw file from MS 
  
_Output:_
- .mzML file

## Run script
If running on Rivanna or other HPC, load required modules. 
```
module load apptainer/1.2.2
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load bioconda/py3.10
module load anaconda/2023.07-py3.11
```
Build a container for msconvert. 
```
mkdir pwiz && cd pwiz
apptainer build --sandbox pwiz docker://chambm/pwiz-skyline-i-agree-to-the-vendor-licenses
mv pwiz/wineprefix64 ./
apptainer build pwiz.sif pwiz 
```
Run msconvert.
```
apptainer exec -B wineprefix64:/wineprefix64 pwiz.sif wine msconvert /project/sheynkman/users/emily/LRP_test/jurkat/00_input_data/mass_spec/120426_Jurkat_highLC_Frac2.raw --filter "peakPicking true 1-"
```

## Proceed to [15 MS File Conversion module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/15_MS_file_convert)
