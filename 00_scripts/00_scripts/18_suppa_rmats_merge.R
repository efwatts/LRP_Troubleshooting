# Load libraries
library(tidyverse)

# Set working directory
setwd("/Volumes/sheynkman/projects/LRP_Mohi_project/")

# Define paths
rmats_path <- "18_SUPPA/rMATS_data/rMATS_all_events_SUPPA_IDs_labeled.tsv"
suppa_path <- "19_LRP_summary/alternative_splice_summary.tsv"
output_dir <- "18_SUPPA/comparison_rmats_vs_suppa"
dir.create(output_dir, showWarnings = FALSE)

# Function to safely load data
safe_load_data <- function(file_path, expected_cols = NULL) {
  if (!file.exists(file_path)) stop(paste("File not found:", file_path))
  cat("Loading:", file_path, "\n")
  data <- read_tsv(file_path, show_col_types = FALSE)
  cat("  - Loaded", nrow(data), "rows and", ncol(data), "columns\n")
  if (!is.null(expected_cols)) {
    missing_cols <- setdiff(expected_cols, colnames(data))
    if (length(missing_cols) > 0) {
      warning(paste("Missing expected columns:", paste(missing_cols, collapse = ", ")))
    }
  }
  return(data)
}

# Load data
rmats <- safe_load_data(rmats_path, c("Event_ID", "Gene", "rMATS_dPSI", "rMATS_FDR", "Event_Type"))
suppa <- safe_load_data(suppa_path, c("Gene", "Event_type", "Coordinates", "WT-Q157R_dPSI", "WT-Q157R_p-val"))

# Filter significant events
rmats_sig <- rmats %>% filter(!is.na(rMATS_FDR), rMATS_FDR < 0.05)
suppa_sig <- suppa %>% filter(!is.na(`WT-Q157R_p-val`), `WT-Q157R_p-val` < 0.05)

# Parse rMATS coordinates
parse_rmats <- function(df) {
  df %>%
    mutate(Event_ID_copy = Event_ID) %>%
    separate(Event_ID, into = c("chr", "exon_range", "strand_up_down"), sep = ":", fill = "right") %>%
    separate(exon_range, into = c("start", "end"), sep = "-", fill = "right") %>%
    mutate(
      start = as.integer(start),
      end = as.integer(end),
      strand = str_sub(strand_up_down, 1, 1)
    ) %>%
    select(chr, start, end, strand, Gene, Event_Type, rMATS_dPSI, rMATS_FDR, rMATS_Event_ID = Event_ID_copy)
}

# Parse SUPPA coordinates
parse_suppa <- function(df) {
  df %>%
    mutate(
      chr = str_extract(Coordinates, "chr[0-9XYM]+"),
      strand = str_extract(Coordinates, "[+-]$")
    ) %>%
    select(chr, strand, Gene, Event_type, Coordinates, `WT-Q157R_dPSI`, `WT-Q157R_p-val`) %>%
    rename(
      SUPPA_dPSI = `WT-Q157R_dPSI`,
      SUPPA_pval = `WT-Q157R_p-val`,
      SUPPA_Event_ID = Coordinates
    )
}

rmats_sig_parsed <- parse_rmats(rmats_sig)
rmats_all_parsed <- parse_rmats(rmats)
suppa_sig_parsed <- parse_suppa(suppa_sig)
suppa_all_parsed <- parse_suppa(suppa)

# 1. Significant rMATS overlapping any SUPPA event
overlap_sig_rmats_all_suppa <- inner_join(
  rmats_sig_parsed, suppa_all_parsed,
  by = c("chr", "strand", "Gene")
)
write_tsv(overlap_sig_rmats_all_suppa, file.path(output_dir, "sig_rmats_all_suppa_overlap.tsv"))

# 2. Significant rMATS overlapping significant SUPPA event
overlap_sig_rmats_sig_suppa <- inner_join(
  rmats_sig_parsed, suppa_sig_parsed,
  by = c("chr", "strand", "Gene")
)
write_tsv(overlap_sig_rmats_sig_suppa, file.path(output_dir, "sig_rmats_sig_suppa_overlap.tsv"))

# 3. All rMATS and all SUPPA events (full reference)
overlap_all_rmats_all_suppa <- full_join(
  rmats_all_parsed, suppa_all_parsed,
  by = c("chr", "strand", "Gene")
)
write_tsv(overlap_all_rmats_all_suppa, file.path(output_dir, "all_rmats_all_suppa.tsv"))

# Summary statistics
n_rmats <- nrow(rmats)
n_rmats_sig <- nrow(rmats_sig)
n_suppa <- nrow(suppa)
n_suppa_sig <- nrow(suppa_sig)
n_overlap_any <- nrow(overlap_sig_rmats_all_suppa)
n_overlap_sig <- nrow(overlap_sig_rmats_sig_suppa)

summary_table <- tibble(
  Category = c(
    "Total rMATS events",
    "Significant rMATS events",
    "Total SUPPA events",
    "Significant SUPPA events",
    "rMATS sig + any SUPPA overlap",
    "rMATS sig + SUPPA sig overlap"
  ),
  Count = c(n_rmats, n_rmats_sig, n_suppa, n_suppa_sig, n_overlap_any, n_overlap_sig)
)
write_tsv(summary_table, file.path(output_dir, "event_overlap_summary.tsv"))

# Scatterplot for ΔPSI correlation
cor_data <- overlap_sig_rmats_sig_suppa %>%
  filter(!is.na(rMATS_dPSI), !is.na(SUPPA_dPSI))

if (nrow(cor_data) >= 5) {
  cor_val <- cor(cor_data$rMATS_dPSI, cor_data$SUPPA_dPSI)
  
  p_scatter <- ggplot(cor_data, aes(x = rMATS_dPSI, y = SUPPA_dPSI)) +
    geom_point(alpha = 0.6) +
    geom_smooth(method = "lm", se = FALSE, color = "blue", linetype = "dashed") +
    labs(
      title = "Correlation of dPSI: rMATS vs SUPPA",
      subtitle = paste0("Pearson r = ", round(cor_val, 3)),
      x = "rMATS ΔPSI",
      y = "SUPPA ΔPSI"
    ) +
    theme_minimal()
  
  ggsave(file.path(output_dir, "dPSI_correlation_plot.pdf"), p_scatter, width = 6, height = 5)
}

# Barplot of counts
p_bar <- ggplot(summary_table, aes(x = reorder(Category, -Count), y = Count)) +
  geom_col(fill = "steelblue") +
  geom_text(aes(label = Count), vjust = -0.5, size = 3.5) +
  labs(title = "Event Counts Summary", x = NULL, y = "Count") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 30, hjust = 1))

ggsave(file.path(output_dir, "event_count_barplot.pdf"), p_bar, width = 7, height = 4.5)

# Completion message
cat("Files written to", output_dir, "\n")