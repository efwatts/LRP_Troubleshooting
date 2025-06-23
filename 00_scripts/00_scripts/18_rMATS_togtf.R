library(tidyverse)
library(readr)

# Set working directory
setwd("/Volumes/sheynkman/projects/LRP_Mohi_project/")

# Read rMATS data
rmats <- read_tsv("18_SUPPA/rMATS_data/rMATS_all_events_SUPPA_IDs_labeled.tsv")

# Parse Event_ID properly to extract all exon coordinates
parsed <- rmats %>%
  mutate(
    event_id = Event_ID,
    # Create safe transcript ID
    transcript_id = gsub("[:@-]", "_", Event_ID)
  ) %>%
  # Split the Event_ID into main event and flanking regions
  separate(Event_ID, into = c("main_event", "flank1", "flank2"), sep = "@", fill = "right") %>%
  # Parse main event (alternative exon)
  separate(main_event, into = c("chr", "alt_coords", "strand"), sep = ":") %>%
  separate(alt_coords, into = c("alt_start", "alt_end"), sep = "-") %>%
  # Parse flanking regions
  separate(flank1, into = c("flank1_start", "flank1_end"), sep = "-") %>%
  separate(flank2, into = c("flank2_start", "flank2_end"), sep = "-") %>%
  # Convert to numeric and clean strand
  mutate(
    across(c(alt_start, alt_end, flank1_start, flank1_end, flank2_start, flank2_end), as.integer),
    strand = str_sub(strand, 1, 1),
    # Create unique gene_id for each event
    unique_gene_id = paste0(Gene, "_", transcript_id)
  )

# Create GTF entries for all exons in each event
gtf_entries <- list()

for(i in 1:nrow(parsed)) {
  row <- parsed[i, ]
  base_attr <- sprintf('gene_id "%s"; transcript_id "%s"; gene_name "%s"; event_id "%s";', 
                       row$unique_gene_id, row$transcript_id, row$Gene, row$event_id)
  
  # Add upstream flanking exon (exon 1)
  if(!is.na(row$flank1_start) && !is.na(row$flank1_end)) {
    gtf_entries[[length(gtf_entries) + 1]] <- data.frame(
      seqname = row$chr,
      source = "rMATS",
      feature = "exon",
      start = row$flank1_start,
      end = row$flank1_end,
      score = ".",
      strand = row$strand,
      frame = ".",
      attribute = paste0(base_attr, ' exon_number "1"; exon_type "flanking_upstream";'),
      stringsAsFactors = FALSE
    )
  }
  
  # Add alternative exon (exon 2)
  gtf_entries[[length(gtf_entries) + 1]] <- data.frame(
    seqname = row$chr,
    source = "rMATS",
    feature = "exon",
    start = row$alt_start,
    end = row$alt_end,
    score = ".",
    strand = row$strand,
    frame = ".",
    attribute = paste0(base_attr, ' exon_number "2"; exon_type "alternative";'),
    stringsAsFactors = FALSE
  )
  
  # Add downstream flanking exon (exon 3)
  if(!is.na(row$flank2_start) && !is.na(row$flank2_end)) {
    gtf_entries[[length(gtf_entries) + 1]] <- data.frame(
      seqname = row$chr,
      source = "rMATS",
      feature = "exon",
      start = row$flank2_start,
      end = row$flank2_end,
      score = ".",
      strand = row$strand,
      frame = ".",
      attribute = paste0(base_attr, ' exon_number "3"; exon_type "flanking_downstream";'),
      stringsAsFactors = FALSE
    )
  }
}

# Combine all entries
gtf_rows <- do.call(rbind, gtf_entries) %>%
  arrange(seqname, start)

# Write GTF with track header
gtf_file <- "18_SUPPA/rmats_events.gtf"

# Write track header first
writeLines("track name=rMATS_events visibility=2 itemRgb=on", gtf_file)

# Append GTF data
write.table(gtf_rows, gtf_file, 
            sep = "\t", quote = FALSE, row.names = FALSE, col.names = FALSE,
            append = TRUE)

cat("Wrote", nrow(gtf_rows), "GTF entries for", nrow(parsed), "rMATS events\n")
cat("Each event includes flanking exons for proper visualization\n")

# Show summary
summary_stats <- gtf_rows %>%
  group_by(seqname) %>%
  summarise(n_exons = n(), .groups = "drop") %>%
  arrange(seqname)

print("Exons per chromosome:")
print(summary_stats)

# Show first few entries for verification
cat("\nFirst few GTF entries:\n")
head(gtf_rows)
