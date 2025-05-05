# This script is based on the edgeR manual - http://www.bioconductor.org/packages/release/bioc/vignettes/edgeR/inst/doc/edgeRUsersGuide.pdf
# and this Stanford tutorial - https://web.stanford.edu/class/bios221/labs/rnaseq/lab_4_rnaseq.html

# Install required packages if not installed
if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager")
if (!requireNamespace("ggplot2", quietly = TRUE)) install.packages("ggplot2")
if (!requireNamespace("readr", quietly = TRUE)) install.packages("readr")

BiocManager::install("edgeR")

# Load libraries
library(edgeR)
library(ggplot2)
library(readr)

# Set working directory
setwd("/Volumes/sheynkman/projects/Mohi_MDS_LRP")

###############################################
################# Transcripts #################
###############################################

# Read in the count data
counts <- read.csv("01_isoseq/collapse/merged.collapsed.flnc_count.txt", header=TRUE, row.names=1)

# Define the sample groups
group <- factor(c("Q157R", "Q157R", "Q157R", "WT", "WT", "WT"))

# Create a DGEList object
dge <- DGEList(counts=counts, group=group)

# Keep transcripts with at least 1 count per million (CPM) in at least 2 samples
keep <- filterByExpr(dge)
dge <- dge[keep, , keep.lib.sizes=FALSE]

# Normalize the data with the TMM method
dge <- calcNormFactors(dge, method = "TMM")

# Create design matrix
design <- model.matrix(~ group)

# Estimate dispersion
dge <- estimateDisp(dge, design)

# Fit the negative binomial model
fit <- glmQLFit(dge, design)
result <- glmQLFTest(fit, coef=2) # compare Q157R to WT

# Extract and save results
deg_results <- topTags(result, n=Inf)$table # Fix: Extract table explicitly
write.table(deg_results, file="19_LRP_summary/edgeR/transcript_DEG_results.txt", sep="\t", quote=FALSE, row.names=TRUE)

# Volcano Plot
deg_results$Gene <- rownames(deg_results) # Add gene column

ggplot(deg_results, aes(x=logFC, y=-log10(PValue))) + 
  geom_point(aes(color=FDR < 0.05)) + 
  scale_color_manual(values=c("black", "red")) + 
  theme_minimal() + 
  labs(title="Volcano Plot", x="Log2 Fold Change", y="-Log10 P-value")

# Save volcano plot
ggsave("19_LRP_summary/edgeR/transcript_volcano_plot.png", width=6, height=6, dpi=300)

###############################################
################### Genes #####################
###############################################

# Read in the count data (Fix: Use read.csv instead of read_table)
counts_gene <- read_delim("/Volumes/sheynkman/projects/Mohi_MDS_LRP/01_isoseq/gene_level_counts.txt", 
                          delim = "\t", escape_double = FALSE, 
                          trim_ws = TRUE)

# Define the sample groups
group_gene <- factor(c("Q157R", "Q157R", "Q157R", "WT", "WT", "WT"))

# Create a DGEList object
dge_gene <- DGEList(counts=counts_gene, group=group_gene)

# Keep genes with at least 1 CPM in at least 2 samples
keep_gene <- filterByExpr(dge_gene)
dge_gene <- dge_gene[keep_gene, , keep.lib.sizes=FALSE]

# Normalize the data with TMM method
dge_gene <- calcNormFactors(dge_gene, method = "TMM")

# Create design matrix
design_gene <- model.matrix(~ group_gene)

# Estimate dispersion
dge_gene <- estimateDisp(dge_gene, design_gene)

# Fit the negative binomial model
fit_gene <- glmQLFit(dge_gene, design_gene)
result_gene <- glmQLFTest(fit_gene, coef=2) # compare Q157R to WT

# Extract and save results
deg_results_gene <- topTags(result_gene, n=Inf)$table # Fix: Extract table explicitly
write.table(deg_results_gene, file="19_LRP_summary/edgeR/gene_DEG_results.txt", sep="\t", quote=FALSE, row.names=TRUE)

# Volcano Plot
deg_results_gene$Gene <- rownames(deg_results_gene) # Add gene column

ggplot(deg_results_gene, aes(x=logFC, y=-log10(PValue))) + 
  geom_point(aes(color=FDR < 0.05)) + 
  scale_color_manual(values=c("black", "red")) + 
  theme_minimal() + 
  labs(title="Volcano Plot", x="Log2 Fold Change", y="-Log10 P-value")

# Save volcano plot
ggsave("19_LRP_summary/edgeR/gene_volcano_plot.png", width=6, height=6, dpi=300)

