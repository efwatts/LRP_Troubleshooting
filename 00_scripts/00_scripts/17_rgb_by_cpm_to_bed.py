#!/usr/bin/env python3

import pandas as pd
import argparse
import os

def hex_to_rgb_tuple(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def cpm_to_rgb(value, min_val, max_val, light_rgb, dark_rgb):
    if pd.isna(value) or max_val == min_val:
        return ",".join(map(str, light_rgb))
    norm = (value - min_val) / (max_val - min_val)
    r = int(light_rgb[0] + (dark_rgb[0] - light_rgb[0]) * norm)
    g = int(light_rgb[1] + (dark_rgb[1] - light_rgb[1]) * norm)
    b = int(light_rgb[2] + (dark_rgb[2] - light_rgb[2]) * norm)
    return f"{r},{g},{b}"

def load_pb_to_ens(sqanti_path):
    try:
        sqanti = pd.read_csv(sqanti_path, sep="\t")
        return sqanti.set_index("isoform")["associated_transcript"].to_dict()
    except Exception as e:
        print(f"Error loading SQANTI table: {e}")
        return {}

def replace_pb_with_ensembl(label, pb_to_ens, cpm_str, frac_str):
    try:
        gene, pb_id, _ = label.split("|")
        enst = pb_to_ens.get(pb_id)
        is_novel = pd.isna(enst) or enst == "novel"
        transcript_id = enst if not is_novel else pb_id
        star = "*" if is_novel else ""
        return f"{gene}|{transcript_id}|{cpm_str}|{frac_str}{star}"
    except Exception:
        return label

def add_rgb_colors(bed_file, light_rgb, dark_rgb, output_file, pb_to_ens):
    bed_names = ['chrom', 'chromStart', 'chromStop', 'acc_full', 'score', 'strand',
                 'thickStart', 'thickEnd', 'itemRGB', 'blockCount', 'blockSizes', 'blockStarts', 'additional_field1']
    bed = pd.read_table(bed_file, names=bed_names, comment='#')
    bed['acc_full'] = bed['acc_full'].astype(str)

    def extract_gene_and_cpm(acc):
        try:
            parts = acc.split('|')
            if len(parts) < 2:
                raise ValueError("Invalid acc_full format")
            gene = parts[0]
            cpm = float(parts[-1])
            return gene, cpm
        except (IndexError, ValueError):
            return None, float("nan")

    bed[['gene', 'cpm']] = bed['acc_full'].apply(lambda x: pd.Series(extract_gene_and_cpm(x)))
    bed = bed.dropna(subset=['gene', 'cpm'])

    bed['gene_total_cpm'] = bed.groupby('gene')['cpm'].transform('sum')
    bed = bed[bed['gene_total_cpm'] > 0]
    bed['frac'] = bed['cpm'] / bed['gene_total_cpm']

    bed['cpm_str'] = bed['cpm'].map(lambda x: f"{x:.2f}")
    bed['frac_str'] = bed['frac'].map(lambda x: f"{x:.2f}")

    min_frac = bed['frac'].min()
    max_frac = bed['frac'].max()
    bed['rgb'] = bed['frac'].apply(lambda x: cpm_to_rgb(x, min_frac, max_frac, light_rgb, dark_rgb))
    bed['score'] = ((bed['frac'] - min_frac) / (max_frac - min_frac) * 1000).fillna(0).astype(int)

    bed['acc_full'] = bed.apply(
        lambda row: replace_pb_with_ensembl(row['acc_full'], pb_to_ens, row['cpm_str'], row['frac_str']),
        axis=1
    )

    int_columns = ['chromStart', 'chromStop', 'score', 'thickStart', 'thickEnd', 'blockCount']
    bed[int_columns] = bed[int_columns].astype(int)
    bed['blockSizes'] = bed['blockSizes'].apply(lambda x: ','.join([str(int(float(i))) for i in x.split(',') if i]))
    bed['blockStarts'] = bed['blockStarts'].apply(lambda x: ','.join([str(int(float(i))) for i in x.split(',') if i]))

    filter_names = ['chrom', 'chromStart', 'chromStop', 'acc_full', 'score', 'strand',
                    'thickStart', 'thickEnd', 'rgb', 'blockCount', 'blockSizes', 'blockStarts']

    with open(output_file, 'w') as ofile:
        ofile.write(f'track name="{os.path.basename(output_file).replace(".bed12", "")}" itemRgb=On\n')
        bed[filter_names].to_csv(ofile, sep='\t', index=None, header=None)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_bed", required=True, help="Input BED13 file with CPM-labeled transcript names")
    parser.add_argument("--day", required=True, choices=['condition1', 'condition2'], help="Specify condition for color gradient")
    parser.add_argument("--output_file", required=True, help="Output BED12 file")
    parser.add_argument("--sqanti", required=True, help="SQANTI classification table for PB → Ensembl mapping")
    args = parser.parse_args()

    BASE_COLORS = {
        "condition1": {
            "light": "#EED8C9",  # light WT
            "dark": "#C94A3F"    # dark WT
        },
        "condition2": {
            "light": "#D4E6F1",  # lighter Q157R
            "dark": "#1D4F72"    # dark Q157R
        }
    }

    light_rgb = hex_to_rgb_tuple(BASE_COLORS[args.day]["light"])
    dark_rgb = hex_to_rgb_tuple(BASE_COLORS[args.day]["dark"])
    pb_to_ens = load_pb_to_ens(args.sqanti)

    add_rgb_colors(args.input_bed, light_rgb, dark_rgb, args.output_file, pb_to_ens)

if __name__ == "__main__":
    main()