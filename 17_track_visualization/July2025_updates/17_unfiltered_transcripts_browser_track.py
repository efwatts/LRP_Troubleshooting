#!/usr/bin/env python3

import pandas as pd
import argparse
import os

def get_rgb_from_scale(value, min_val, max_val, rgb_scale):
    """Get RGB color from predefined scale based on normalized value"""
    if pd.isna(value) or max_val == min_val:
        return rgb_scale[-1]  # Return lightest color (pale pink) for NaN or no variation
    
    norm = (value - min_val) / (max_val - min_val)
    # Invert the scale so high values get dark colors (index 0) and low values get light colors (index -1)
    index = int((1 - norm) * (len(rgb_scale) - 1))
    index = max(0, min(index, len(rgb_scale) - 1))  # Ensure index is within bounds
    return rgb_scale[index]

def load_cpm_data(cpm_file_path):
    """Load CPM data from TSV file and return mapping dictionaries"""
    try:
        cpm_df = pd.read_csv(cpm_file_path, sep="\t")
        
        # Check required columns
        required_columns = ['pb_acc', 'gene', 'mean_CPM']
        missing_cols = [col for col in required_columns if col not in cpm_df.columns]
        if missing_cols:
            raise ValueError(f"CPM file must have columns: {required_columns}. Missing: {missing_cols}")
        
        # Create mapping dictionaries
        pb_to_gene_mapping = cpm_df.set_index("pb_acc")["gene"].to_dict()
        pb_to_cpm = cpm_df.set_index("pb_acc")["mean_CPM"].to_dict()
        
        # Also create transcript_id mapping if it exists
        pb_to_transcript = {}
        if 'transcript_id' in cpm_df.columns:
            pb_to_transcript = cpm_df.set_index("pb_acc")["transcript_id"].to_dict()
        
        return pb_to_gene_mapping, pb_to_cpm, pb_to_transcript
        
    except Exception as e:
        print(f"Error loading CPM data file: {e}")
        return {}, {}, {}

def make_acc_label_with_pb(gene, pb_id, cpm_str, frac_str, pb_to_transcript):
    """Create label with gene, PB ID, CPM, and fraction info"""
    transcript_id = pb_to_transcript.get(pb_id, "")
    is_novel = not transcript_id or transcript_id == "novel" or pd.isna(transcript_id)
    star = "*" if is_novel else ""
    return f"{gene}|{pb_id}|{cpm_str}|{frac_str}{star}"

def add_rgb_colors_from_cpm(bed_file, output_file, pb_to_gene_mapping, pb_to_cpm, pb_to_transcript, rgb_scale):
    """Process BED file and add RGB colors based on CPM data"""
    bed_names = ['chrom', 'chromStart', 'chromStop', 'acc_full', 'score', 'strand',
                 'thickStart', 'thickEnd', 'itemRGB', 'blockCount', 'blockSizes', 'blockStarts']
    
    # Handle potential additional columns
    try:
        bed = pd.read_table(bed_file, names=bed_names + ['additional_field1'], comment='#')
    except:
        bed = pd.read_table(bed_file, names=bed_names, comment='#')
    
    bed['acc_full'] = bed['acc_full'].astype(str)

    def extract_pb_id(acc):
        """Extract PacBio ID from acc_full field"""
        try:
            # Assuming acc_full contains PB.ID or similar format
            parts = acc.split('|')
            if len(parts) >= 2:
                return parts[1]  # Assume PB ID is second element
            else:
                # If no pipe separator, assume the whole string is the PB ID
                return acc
        except:
            return acc

    # Extract PB IDs and get gene/CPM info
    bed['pb_id'] = bed['acc_full'].apply(extract_pb_id)
    bed['gene'] = bed['pb_id'].map(pb_to_gene_mapping)
    bed['cpm'] = bed['pb_id'].map(pb_to_cpm)
    
    # Filter out transcripts not found in CPM data
    bed = bed.dropna(subset=['gene', 'cpm'])
    
    if bed.empty:
        print("Warning: No transcripts found in CPM data.")
        print("Check if BED file PB IDs match the pb_acc column in CPM file.")
        return
    
    # Calculate gene-level totals and fractions
    bed['gene_total_cpm'] = bed.groupby('gene')['cpm'].transform('sum')
    bed = bed[bed['gene_total_cpm'] > 0]
    bed['frac'] = bed['cpm'] / bed['gene_total_cpm']

    # Format strings for display
    bed['cpm_str'] = bed['cpm'].map(lambda x: f"{x:.2f}")
    bed['frac_str'] = bed['frac'].map(lambda x: f"{x:.2f}")

    # Apply RGB gradient to itemRGB based on fraction using predefined scale
    min_frac = bed['frac'].min()
    max_frac = bed['frac'].max()
    bed['itemRGB'] = bed['frac'].apply(lambda x: get_rgb_from_scale(x, min_frac, max_frac, rgb_scale))

    # Score based on fraction (0-1000 scale)
    bed['score'] = ((bed['frac'] - min_frac) / (max_frac - min_frac) * 1000).fillna(0).astype(int)

    # Update acc_full with gene, PB ID, CPM, and fraction info
    bed['acc_full'] = bed.apply(
        lambda row: make_acc_label_with_pb(row['gene'], row['pb_id'], row['cpm_str'], row['frac_str'], pb_to_transcript),
        axis=1
    )

    # Convert numeric columns to appropriate types
    int_columns = ['chromStart', 'chromStop', 'score', 'thickStart', 'thickEnd', 'blockCount']
    bed[int_columns] = bed[int_columns].astype(int)
    
    # Handle block sizes and starts (convert floats to ints if needed)
    bed['blockSizes'] = bed['blockSizes'].apply(lambda x: ','.join([str(int(float(i))) for i in str(x).split(',') if i]))
    bed['blockStarts'] = bed['blockStarts'].apply(lambda x: ','.join([str(int(float(i))) for i in str(x).split(',') if i]))

    # Output columns for BED12 format
    output_columns = ['chrom', 'chromStart', 'chromStop', 'acc_full', 'score', 'strand',
                     'thickStart', 'thickEnd', 'itemRGB', 'blockCount', 'blockSizes', 'blockStarts']

    # Write output file
    with open(output_file, 'w') as ofile:
        ofile.write(f"track name=\"{os.path.basename(output_file).replace('.bed', '')}\" itemRgb=On\n")
        bed[output_columns].to_csv(ofile, sep='\t', index=None, header=None)
    
    print(f"Processed {len(bed)} transcripts from {bed['gene'].nunique()} genes")
    print(f"CPM range: {bed['cpm'].min():.2f} - {bed['cpm'].max():.2f}")
    print(f"Fraction range: {min_frac:.3f} - {max_frac:.3f}")

def main():
    parser = argparse.ArgumentParser(description="Color BED transcripts by abundance from CPM data file")
    parser.add_argument("--input_bed", required=True, help="Input BED file with transcript coordinates")
    parser.add_argument("--output_file", required=True, help="Output BED12 file with RGB colors")
    parser.add_argument("--cpm_file", required=True, help="TSV file with pb_acc, gene, and mean_CPM columns")
    args = parser.parse_args()

    # Pink to black color scale (pale pink to black)
    rgb_scale = [
        '0,0,0', '26,0,0', '51,0,0', '77,0,0', '102,0,0',
        '128,0,0', '153,0,0', '179,0,0', '204,0,0', '230,0,0',
        '255,0,0', '255,26,26', '255,51,51', '255,77,77', '255,102,102',
        '255,128,128', '255,153,153', '255,179,179', '255,204,204', '255,230,230'
    ]
    
    # Load CPM data
    pb_to_gene_mapping, pb_to_cpm, pb_to_transcript = load_cpm_data(args.cpm_file)
    
    if not pb_to_cpm:
        print("Error: Could not load CPM data")
        return 1
    
    # Process BED file and add colors
    add_rgb_colors_from_cpm(args.input_bed, args.output_file, 
                           pb_to_gene_mapping, pb_to_cpm, pb_to_transcript, rgb_scale)
    
    print(f"Output written to: {args.output_file}")
    return 0

if __name__ == "__main__":
    exit(main())