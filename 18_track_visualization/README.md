# Track Visualization
Prepare data to be viewed in [UCSC Genome Browser](https://genome.ucsc.edu/) <br />
For another approach, see my repository [here](https://github.com/efwatts/PoGo2GenomeBrowser)

_Input:_ <br />
- [Gencode](https://www.gencodegenes.org/) GTF file
- cds.gtf (from [07 Make CDS GTF module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/07_make_cds_gtf)
- accession_map_gencode_uniprot_pacbio.tsv (from [15 Accession Mapping module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/15_accession_mapping))
- filtered.gtf (from [13 Protein Filter module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/13_protein_filter))
- high_confidence.gtf (from [14 Make Hybrid Database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/14_make_hybrid_database))
- AllPeptides.sample.psmtsv (refined, hybrid, and filtered) (from [16 MetaMorpheus module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/16_MetaMorpheus))
- pb_gene.tsv (from [04 Transcriptome Summary module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/04_transcriptome_summary))
- gene_isoname (from [01 Reference Tables module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/01_reference_tables))
- hybrid.fasta (from [14 Make Hybrid Database module](https://github.com/efwatts/LRP_Troubleshooting/tree/main/14_make_hybrid_database))
  
_Output:_
- peptide/hybrid_peptides.bed12
- peptide/hybrid_shaded_peptides.bed12
- multiregion_bed/filtered_ucsc_multiregion.bed
- multiregion_bed/hybrid_ucsc_multiregion.bed
- multiregion_bed/refined_ucsc_multiregion.bed
- protein/filtered_cds.bed12
- protein/filtered_cds.genePred
- protein/filtered_shaded_cpm.bed12
- protein/filtered_shaded_protein_class.bed12
- protein/hybrid_cds.bed12
- protein/hybrid_cds.genePred
- protein/hybrid_shaded_cpm.bed12
- protein/hybrid_shaded_protein_class.bed12
- protein/refined_cds.bed12
- protein/refined_cds.genePred
- protein/refined_shaded_cpm.bed12
- protein/refined_shaded_protein_class.bed12
  
## Run scripts
#### Reference Track Visualization
Create environment and load necessary modules
```
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load bioconda/py3.10
module load anaconda/2023.07-py3.11

conda env create -f ./00_environments/visualization.yml 
conda activate visualization
```
Run gencode_filter_protein_coding.py and gtfToGenePred, genePredToBed, and gencode_add_rgb_to_bed.py
```
python ./00_scripts/18_gencode_filter_protein_coding.py \
--reference_gtf ./00_input_data/gencode.v35.annotation.canonical.gtf \
--output_dir ./18_track_visualization/reference

gtfToGenePred ./18_track_visualization/reference/gencode.filtered.gtf ./18_track_visualization/reference/gencode.filtered.genePred

genePredToBed ./18_track_visualization/reference/gencode.filtered.genePred ./18_track_visualization/reference/gencode.filtered.bed12

python ./00_scripts/18_gencode_add_rgb_to_bed.py \
--gencode_bed ./18_track_visualization/reference/gencode.filtered.bed12 \
--rgb 0,0,140 \
--version V35 \
--output_dir ./18_track_visualization/reference
```

#### Protein Track Visualization
Use the same loaded environment and modules.
Can do this with each database type (refined, filtered, hybrid)
```
# Refined
gtfToGenePred ./00_test_data/jurkat_with_cds.gtf ./18_track_visualization/protein/jurkat_refined_cds.genePred
genePredToBed ./18_track_visualization/protein/jurkat_refined_cds.genePred ./18_track_visualization/protein/jurkat_refined_cds.bed12

python ./00_scripts/18_track_add_rgb_colors_to_bed.py \
--name ./18_track_visualization/protein/jurkat_refined \
--bed_file ./18_track_visualization/protein/jurkat_refined_cds.bed12

# Filtered
gtfToGenePred ./13_protein_filter/jurkat_with_cds_filtered.gtf ./18_track_visualization/protein/jurkat_filtered_cds.genePred
genePredToBed ./18_track_visualization/protein/jurkat_filtered_cds.genePred ./18_track_visualization/protein/jurkat_filtered_cds.bed12
 
python ./00_scripts/18_track_add_rgb_colors_to_bed.py \
--name ./18_track_visualization/protein/jurkat_filtered \
--bed_file ./18_track_visualization/protein/jurkat_filtered_cds.bed12

# Hybrid
gtfToGenePred ./14_protein_hybrid_database/jurkat_cds_high_confidence.gtf ./18_track_visualization/protein/jurkat_hybrid_cds.genePred
genePredToBed ./18_track_visualization/protein/jurkat_hybrid_cds.genePred ./18_track_visualization/protein/jurkat_hybrid_cds.bed12

python ./00_scripts/18_track_add_rgb_colors_to_bed.py \
--name ./18_track_visualization/protein/jurkat_hybrid \
--bed_file ./18_track_visualization/protein/jurkat_hybrid_cds.bed12
```

#### Multiregion BED generation
Leave the same environment and modules loaded

```
# Refined
python ./00_scripts/18_make_region_bed_for_ucsc.py \
--name jurkat_refined \
--sample_gtf ./07_make_cds_gtf/jurkat_with_cds.gtf \
--reference_gtf ./00_input_data/gencode.v35.annotation.canonical.gtf \
--output_dir ./18_track_visualization/multiregion_bed

# Filtered
python ./00_scripts/18_make_region_bed_for_ucsc.py \
--name jurkat_filtered \
--sample_gtf ./13_protein_filter/jurkat_with_cds_filtered.gtf \
--reference_gtf ./00_input_data/gencode.v35.annotation.canonical.gtf \
--output_dir ./18_track_visualization/multiregion_bed

# Hybrid
python ./00_scripts/18_make_region_bed_for_ucsc.py \
--name jurkat_hybrid \
--sample_gtf ./14_protein_hybrid_database/jurkat_cds_high_confidence.gtf \
--reference_gtf ./00_input_data/gencode.v35.annotation.canonical.gtf \
--output_dir ./18_track_visualization/multiregion_bed
```
Done!

#### Peptide Track Visualization
Leave the same environment and modules loaded
```
# Hyrbid
python ./00_scripts/18_make_peptide_gtf_file.py \
--name ./18_track_visualization/peptide/jurkat_hybrid \
--sample_gtf ./14_protein_hybrid_database/jurkat_cds_high_confidence.gtf \
--reference_gtf ./00_input_data/gencode.v35.annotation.canonical.gtf \
--peptides ./16_MetaMorpheus/hybrid/Task1SearchTask/AllPeptides.psmtsv \
--pb_gene ./04_transcriptome_summary/pb_gene.tsv \
--gene_isoname ./01_reference_tables/gene_isoname.tsv \
--refined_fasta ./13_protein_hybrid_database/jurkat_hybrid.fasta 

gtfToGenePred ./18_track_visualization/peptide/jurkat_hybrid_peptides.gtf ./18_track_visualization/peptide/jurkat_hybrid_peptides.genePred
genePredToBed ./18_track_visualization/peptide/jurkat_hybrid_peptides.genePred ./18_track_visualization/peptide/jurkat_hybrid_peptides.bed12
# add rgb to colorize specific peptides
python ./00_scripts/18_finalize_peptide_bed.py \
--bed ./18_track_visualization/peptide/jurkat_hybrid_peptides.bed12 \
--name ./18_track_visualization/jurkat_hybrid

conda deactivate
```

## Proceed to
