
#!/usr/bin/env python3

import pandas as pd
import glob
import os
import argparse
import matplotlib.pyplot as plt

# Set thresholds
PERC_A_THRESHOLD = 80
CODING_SCORE_THRESHOLD = 0.364
ALLOWED_STRUCTURAL_CATEGORIES = {
    "novel_not_in_catalog", "novel_in_catalog", "incomplete-splice_match", "full-splice_match"
}

# Mapping dropout file patterns
dropout_file_info = {
    "dropout_*classification.txt": ("SQANTI Filtering", "sqanti_classification"),
    "dropout_*collapsed_classification.tsv": ("SQANTI Filtering", "collapse_classification"),
    "dropout_*cpat.tsv": ("CPAT Filtering", "cpat"),
    "dropout_*orf.tsv": ("ORF Refinement", "orf")
}

# Prettier label mapping
prettier_labels = {
    "Non-coding gene": "Non-coding gene",
    "Template switching artifact": "RTS artifact",
    "Intra-priming (polyA downstream)": "Intra-priming",
    "Bad structural category": "Bad structure",
    "Dropped during collapse (no match)": "Collapse - no match",
    "Low coding probability": "Low coding prob.",
    "Low coding score": "Low coding score",
    "No stop codon": "No stop codon",
    "Unknown SQANTI filter": "Misc (SQANTI)",
    "Unknown CPAT filter": "Misc (CPAT)",
    "Unknown ORF filter": "Misc (ORF)",
    "Unknown reason": "Misc"
}

def determine_sqanti_reason(row):
    reasons = []
    if pd.isna(row.get("associated_gene", None)):
        reasons.append("Non-coding gene")
    if row.get("RTS_stage", False) == True:
        reasons.append("Template switching artifact")
    if row.get("perc_A_downstream_TTS", 0) > PERC_A_THRESHOLD:
        reasons.append("Intra-priming (polyA downstream)")
    if row.get("structural_category", "") not in ALLOWED_STRUCTURAL_CATEGORIES:
        reasons.append("Bad structural category")
    return "; ".join(reasons) if reasons else "Unknown SQANTI filter"

def determine_collapse_reason(_row):
    return "Dropped during collapse (no match)"

def determine_cpat_reason(row):
    if row.get("coding_score", 1) < CODING_SCORE_THRESHOLD:
        return "Low coding probability"
    return "Unknown CPAT filter"

def determine_orf_reason(row):
    reasons = []
    if row.get("coding_score", 1) < CODING_SCORE_THRESHOLD:
        reasons.append("Low coding score")
    if not row.get("has_stop_codon", True):
        reasons.append("No stop codon")
    return "; ".join(reasons) if reasons else "Unknown ORF filter"

def map_pretty_label(label):
    return prettier_labels.get(label, "Misc")

def collect_dropouts(dropout_dir):
    all_dropouts = []

    for pattern, (step, filetype) in dropout_file_info.items():
        full_pattern = os.path.join(dropout_dir, pattern)
        matched_files = glob.glob(full_pattern)

        for file in matched_files:
            if file.endswith(".tsv") or file.endswith(".txt"):
                try:
                    df = pd.read_csv(file, sep="\t")
                except:
                    df = pd.read_csv(file, sep="\t", header=None)

                if "isoform" in df.columns:
                    id_col = "isoform"
                elif "pb_acc" in df.columns:
                    id_col = "pb_acc"
                elif "ID" in df.columns:
                    id_col = "ID"
                else:
                    id_col = df.columns[0]

                for idx, row in df.iterrows():
                    transcript_id = row[id_col]
                    if filetype == "sqanti_classification":
                        reason = determine_sqanti_reason(row)
                    elif filetype == "collapse_classification":
                        reason = determine_collapse_reason(row)
                    elif filetype == "cpat":
                        reason = determine_cpat_reason(row)
                    elif filetype == "orf":
                        reason = determine_orf_reason(row)
                    else:
                        reason = "Unknown reason"

                    all_dropouts.append((transcript_id, step, reason))

    return pd.DataFrame(all_dropouts, columns=["Transcript_ID", "Step", "Specific_Reason"])

def summarize_dropouts(dropout_df, output_prefix):
    dropout_df = dropout_df.drop_duplicates(subset=["Transcript_ID"])

    # Map prettier labels
    dropout_df["Pretty_Reason"] = dropout_df["Specific_Reason"].apply(lambda x: map_pretty_label(x))

    dropout_df.to_csv(f"{output_prefix}_dropout_summary_detailed.tsv", sep="\t", index=False)

    # Global barplot
    reason_counts = dropout_df["Pretty_Reason"].value_counts()
    plt.figure(figsize=(12, 6))
    reason_counts.plot(kind="bar")
    plt.title("Number of Dropouts by Specific Reason (All Steps)")
    plt.ylabel("Number of Dropouts")
    plt.xlabel("Specific Reason")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(f"{output_prefix}_dropout_summary_detailed_barplot.png")
    plt.close()

    # Global pie chart
    plt.figure(figsize=(8, 8))
    reason_counts.plot(kind="pie", autopct="%1.1f%%", startangle=140)
    plt.ylabel("")
    plt.title("Dropout Reasons Distribution (All Steps)")
    plt.tight_layout()
    plt.savefig(f"{output_prefix}_dropout_summary_detailed_piechart.png")
    plt.close()

    # Separate pie charts per step
    for step in dropout_df["Step"].unique():
        step_df = dropout_df[dropout_df["Step"] == step]
        step_reason_counts = step_df["Pretty_Reason"].value_counts()

        plt.figure(figsize=(8, 8))
        step_reason_counts.plot(kind="pie", autopct="%1.1f%%", startangle=140)
        plt.ylabel("")
        plt.title(f"Dropout Reasons for {step}")
        plt.tight_layout()

        safe_step = step.replace(" ", "_").replace("(", "").replace(")", "")
        plt.savefig(f"{output_prefix}_dropout_summary_detailed_piechart_{safe_step}.png")
        plt.close()

def main():
    parser = argparse.ArgumentParser(description="Summarize detailed transcript dropouts with prettier labels and pie charts per step.")
    parser.add_argument("--dropout_dir", required=True, help="Directory containing dropout files.")
    parser.add_argument("--output_prefix", required=True, help="Output prefix for summary files.")

    args = parser.parse_args()

    dropout_df = collect_dropouts(args.dropout_dir)
    summarize_dropouts(dropout_df, args.output_prefix)

    print(f"Detailed dropout summary complete with prettier labels. Summary and plots saved with prefix {args.output_prefix}.")

if __name__ == "__main__":
    main()
