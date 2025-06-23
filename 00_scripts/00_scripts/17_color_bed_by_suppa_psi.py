#!/usr/bin/env python3

import pandas as pd
import argparse
import math

# Coarse redscale RGB gradient (light to dark)
rgb_scale = [
    '0,0,0', '26,0,0', '51,0,0', '77,0,0', '102,0,0',
    '128,0,0', '153,0,0', '179,0,0', '204,0,0', '230,0,0',
    '255,0,0', '255,26,26', '255,51,51', '255,77,77', '255,102,102',
    '255,128,128', '255,153,153', '255,179,179', '255,204,204', '255,230,230'
]

def parse_args():
    parser = argparse.ArgumentParser(description="Color BED12 based on SUPPA PSI values")
    parser.add_argument('--input_bed', required=True)
    parser.add_argument('--psi_summary', required=True)
    parser.add_argument('--event_type', required=True, help='SE, RI, A3, A5, MX, AF, AL')
    parser.add_argument('--output_prefix', required=True)
    parser.add_argument('--psi_column_wt', default='avg_PSI_WT')
    parser.add_argument('--psi_column_mutant', default='avg_PSI_Q157R')
    parser.add_argument('--pval_column', default='WT-Q157R_p-val')
    parser.add_argument('--pval_threshold', type=float, default=0.05)
    return parser.parse_args()

def psi_to_rgb(psi):
    if pd.isna(psi):
        return '0,0,0'
    bin_idx = min(int(psi * (len(rgb_scale) - 1)), len(rgb_scale) - 1)
    return rgb_scale[::-1][bin_idx]

def get_coords_from_name(name_field):
    return name_field.split(':alternative')[0].split(':', 1)[1]  # Remove type prefix (e.g. RI:) and suffix

def generate_bed(output_path, coord_to_psi, input_bed, label):
    output_lines = [f'track name="{label}" itemRgb="On"']
    with open(input_bed) as f:
        for line in f:
            if line.startswith('track'):
                continue
            fields = line.strip().split('\t')
            if len(fields) < 12:
                continue

            name_field = fields[3]
            coord_key = get_coords_from_name(name_field)
            if coord_key in coord_to_psi:
                psi_incl = coord_to_psi[coord_key]['psi']
                pval = coord_to_psi[coord_key]['pval']

                if name_field.endswith('alternative1'):
                    psi = psi_incl
                elif name_field.endswith('alternative2'):
                    psi = 1 - psi_incl
                else:
                    continue

                if pd.isna(psi):
                    continue

                sig_marker = '*' if pval < 0.05 else ''
                rgb = psi_to_rgb(psi)
                fields[3] = f"{name_field}|{round(psi, 3)}{sig_marker}"
                fields[4] = '0'
                fields[8] = rgb
                output_lines.append('\t'.join(fields))

    with open(output_path, 'w') as out:
        for line in output_lines:
            out.write(line + '\n')

def main():
    args = parse_args()

    psi_df = pd.read_csv(args.psi_summary, sep='\t', low_memory=False)
    psi_df = psi_df[psi_df['Event_type'].str.upper() == args.event_type.upper()].copy()
    psi_df = psi_df.drop_duplicates(subset='Coordinates', keep='first')

    psi_df[args.psi_column_wt] = pd.to_numeric(psi_df[args.psi_column_wt], errors='coerce')
    psi_df[args.psi_column_mutant] = pd.to_numeric(psi_df[args.psi_column_mutant], errors='coerce')
    psi_df[args.pval_column] = pd.to_numeric(psi_df[args.pval_column], errors='coerce')

    psi_df['abs_wt'] = psi_df[args.psi_column_wt].abs().clip(0, 1)
    psi_df['rgb_wt'] = psi_df['abs_wt'].apply(psi_to_rgb)
    coord_to_wt = psi_df.set_index('Coordinates')[[args.psi_column_wt, args.pval_column]].copy()
    coord_to_wt['psi'] = coord_to_wt[args.psi_column_wt]
    coord_to_wt['pval'] = psi_df.set_index('Coordinates')[args.pval_column]
    coord_to_wt['rgb'] = psi_df.set_index('Coordinates')['rgb_wt']

    psi_df['abs_mut'] = psi_df[args.psi_column_mutant].abs().clip(0, 1)
    psi_df['rgb_mut'] = psi_df['abs_mut'].apply(psi_to_rgb)
    coord_to_mut = psi_df.set_index('Coordinates')[[args.psi_column_mutant, args.pval_column]].copy()
    coord_to_mut['psi'] = coord_to_mut[args.psi_column_mutant]
    coord_to_mut['pval'] = psi_df.set_index('Coordinates')[args.pval_column]
    coord_to_mut['rgb'] = psi_df.set_index('Coordinates')['rgb_mut']

    generate_bed(args.output_prefix + '_WT.bed12', coord_to_wt.to_dict(orient='index'), args.input_bed, f"{args.event_type}_WT")
    generate_bed(args.output_prefix + '_Q157R.bed12', coord_to_mut.to_dict(orient='index'), args.input_bed, f"{args.event_type}_Q157R")

if __name__ == '__main__':
    main()