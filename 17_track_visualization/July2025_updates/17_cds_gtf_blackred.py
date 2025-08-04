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

def parse_bed_name(name_field):
    """Parse the name field to extract gene, PB ID, and CPM"""
    parts = name_field.split('|')
    if len(parts) >= 3:
        gene = parts[0]
        pb_id = parts[1]
        cpm = float(parts[2])
        return gene, pb_id, cpm
    else:
        raise ValueError(f"Invalid name field format: {name_field}. Expected GENE|PBID|CPM")

def process_bed_file(bed_file, output_file, rgb_scale):
    """Process BED file and add colors based on transcript fractions within genes"""
    
    bed_columns = ['chrom', 'chromStart', 'chromEnd', 'name', 'score', 'strand',
                   'thickStart', 'thickEnd', 'itemRgb', 'blockCount', 'blockSizes', 'blockStarts']
    
    # Read BED file
    bed = pd.read_csv(bed_file, sep='\t', names=bed_columns, comment='#')
    
    # Parse name field to extract gene, PB ID, and CPM
    parsed_data = bed['name'].apply(parse_bed_name)
    bed['gene'] = parsed_data.apply(lambda x: x[0])
    bed['pb_id'] = parsed_data.apply(lambda x: x[1])
    bed['cpm'] = parsed_data.apply(lambda x: x[2])
    
    # Calculate gene-level totals and fractions
    bed['gene_total_cpm'] = bed.groupby('gene')['cpm'].transform('sum')
    bed = bed[bed['gene_total_cpm'] > 0]  # Remove genes with 0 total CPM
    bed['frac'] = bed['cpm'] / bed['gene_total_cpm']
    
    # Format strings for display
    bed['cpm_str'] = bed['cpm'].map(lambda x: f"{x:.2f}")
    bed['frac_str'] = bed['frac'].map(lambda x: f"{x:.2f}")
    
    # Create new name field with Gene|PB|CPM|Frac format
    bed['new_name'] = bed.apply(
        lambda row: f"{row['gene']}|{row['pb_id']}|{row['cpm_str']}|{row['frac_str']}",
        axis=1
    )
    
    # Calculate RGB colors based on fractions
    min_frac = bed['frac'].min()
    max_frac = bed['frac'].max()
    bed['itemRgb'] = bed['frac'].apply(
        lambda x: get_rgb_from_scale(x, min_frac, max_frac, rgb_scale)
    )
    
    # Update score based on fraction (0-1000 scale)
    bed['score'] = ((bed['frac'] - min_frac) / (max_frac - min_frac) * 1000).fillna(0).astype(int)
    
    # Convert numeric columns to appropriate types
    int_columns = ['chromStart', 'chromEnd', 'score', 'thickStart', 'thickEnd', 'blockCount']
    bed[int_columns] = bed[int_columns].astype(int)
    
    # Handle block sizes and starts (convert floats to ints if needed)
    bed['blockSizes'] = bed['blockSizes'].apply(lambda x: ','.join([str(int(float(i))) for i in str(x).split(',') if i]))
    bed['blockStarts'] = bed['blockStarts'].apply(lambda x: ','.join([str(int(float(i))) for i in str(x).split(',') if i]))
    
    # Prepare output columns
    output_columns = ['chrom', 'chromStart', 'chromEnd', 'new_name', 'score', 'strand',
                      'thickStart', 'thickEnd', 'itemRgb', 'blockCount', 'blockSizes', 'blockStarts']
    
    # Write output file
    with open(output_file, 'w') as ofile:
        ofile.write(f"track name=\"{os.path.basename(output_file).replace('.bed', '')}\" itemRgb=On\n")
        bed[output_columns].to_csv(ofile, sep='\t', index=False, header=False)
    
    print(f"Processed {len(bed)} transcripts from {bed['gene'].nunique()} genes")
    print(f"CPM range: {bed['cpm'].min():.2f} - {bed['cpm'].max():.2f}")
    print(f"Fraction range: {min_frac:.3f} - {max_frac:.3f}")
    print(f"Color range: {bed['itemRgb'].iloc[bed['frac'].idxmax()]} (high) to {bed['itemRgb'].iloc[bed['frac'].idxmin()]} (low)")

def main():
    parser = argparse.ArgumentParser(description="Color BED transcripts by abundance fractions within genes")
    parser.add_argument("--input_bed", required=True, help="Input BED file with GENE|PBID|CPM format in name field")
    parser.add_argument("--output_file", required=True, help="Output BED12 file with RGB colors and updated labels")
    args = parser.parse_args()

    # Pink to black color scale (pale pink to black)
    rgb_scale = [
        '0,0,0', '26,0,0', '51,0,0', '77,0,0', '102,0,0',
        '128,0,0', '153,0,0', '179,0,0', '204,0,0', '230,0,0',
        '255,0,0', '255,26,26', '255,51,51', '255,77,77', '255,102,102',
        '255,128,128', '255,153,153', '255,179,179', '255,204,204', '255,230,230'
    ]
    
    # Process BED file and add colors
    process_bed_file(args.input_bed, args.output_file, rgb_scale)
    
    print(f"Output written to: {args.output_file}")
    return 0

if __name__ == "__main__":
    exit(main())