#!/usr/bin/env python3

import pandas as pd
import argparse
import os

def hex_to_rgb_tuple(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def load_sqanti_data(sqanti_path):
    try:
        sqanti = pd.read_csv(sqanti_path, sep="\t")
        pb_to_ens = sqanti.set_index("pb")["pr_transcripts"].to_dict()
        raw_cat = sqanti.set_index("pb")["pr_splice_cat"].to_dict()
        cat_map = {
            "novel_not_in_catalog": "pNNC",
            "novel_in_catalog": "pNIC",
            "full-splice_match": "pFSM",
            "incomplete-splice_match": "pISM",
            "fusion": "pFUS",
            "intergenic": "pINT",
        }
        pb_to_category = {pbid: cat_map.get(cat, "Other") for pbid, cat in raw_cat.items()}
        return pb_to_ens, pb_to_category
    except Exception as e:
        print(f"Error loading SQANTI table: {e}")
        return {}, {}

def cpm_to_rgb(value, min_val, max_val, light_rgb, dark_rgb):
    if pd.isna(value) or max_val == min_val:
        return ",".join(map(str, light_rgb))
    norm = (value - min_val) / (max_val - min_val)
    r = int(light_rgb[0] + (dark_rgb[0] - light_rgb[0]) * norm)
    g = int(light_rgb[1] + (dark_rgb[1] - light_rgb[1]) * norm)
    b = int(light_rgb[2] + (dark_rgb[2] - light_rgb[2]) * norm)
    return f"{r},{g},{b}"

def make_acc_label_with_pb(gene, pb_id, cpm_str, frac_str, pb_to_ens, pb_to_category):
    enst = pb_to_ens.get(pb_id)
    category = pb_to_category.get(pb_id, "Other")
    is_novel = pd.isna(enst) or enst == "novel"
    star = "*" if is_novel else ""
    return f"{gene}|{pb_id}|{category}|{cpm_str}|{frac_str}{star}"

def extract_gene_pb_cpm(acc):
    try:
        parts = acc.split('|')
        if len(parts) < 3:
            raise ValueError("Invalid acc_full format")
        gene = parts[0]
        pb_id = parts[1]
        cpm = float(parts[2])
        return gene, pb_id, cpm
    except (IndexError, ValueError):
        return None, None, float("nan")

def add_rgb_colors(bed_file, light_rgb, dark_rgb, output_file, pb_to_ens, pb_to_category):
    bed_names = ['chrom', 'chromStart', 'chromStop', 'acc_full', 'score', 'strand',
                 'thickStart', 'thickEnd', 'itemRGB', 'blockCount', 'blockSizes', 'blockStarts', 'additional_field1']
    bed = pd.read_table(bed_file, names=bed_names, comment='#')
    bed['acc_full'] = bed['acc_full'].astype(str)

    parsed = bed['acc_full'].apply(lambda x: pd.Series(extract_gene_pb_cpm(x)))
    parsed.columns = ['gene', 'tx_id', 'cpm']
    bed = pd.concat([bed, parsed], axis=1)
    bed = bed.dropna(subset=['gene', 'tx_id', 'cpm'])

    bed['gene_total_cpm'] = bed.groupby('gene')['cpm'].transform('sum')
    bed = bed[bed['gene_total_cpm'] > 0]
    bed['frac'] = bed['cpm'] / bed['gene_total_cpm']

    bed['cpm_str'] = bed['cpm'].map(lambda x: f"{x:.2f}")
    bed['frac_str'] = bed['frac'].map(lambda x: f"{x:.2f}")

    min_frac = bed['frac'].min()
    max_frac = bed['frac'].max()
    bed['itemRGB'] = bed['frac'].apply(lambda x: cpm_to_rgb(x, min_frac, max_frac, light_rgb, dark_rgb))

    bed['score'] = ((bed['frac'] - min_frac) / (max_frac - min_frac) * 1000).fillna(0).astype(int)

    bed['acc_full'] = bed.apply(
        lambda row: make_acc_label_with_pb(row['gene'], row['tx_id'], row['cpm_str'], row['frac_str'], pb_to_ens, pb_to_category),
        axis=1
    )

    int_columns = ['chromStart', 'chromStop', 'score', 'thickStart', 'thickEnd', 'blockCount']
    bed[int_columns] = bed[int_columns].astype(int)
    bed['blockSizes'] = bed['blockSizes'].apply(lambda x: ','.join([str(int(float(i))) for i in x.split(',') if i]))
    bed['blockStarts'] = bed['blockStarts'].apply(lambda x: ','.join([str(int(float(i))) for i in x.split(',') if i]))

    filter_names = ['chrom', 'chromStart', 'chromStop', 'acc_full', 'score', 'strand',
                    'thickStart', 'thickEnd', 'itemRGB', 'blockCount', 'blockSizes', 'blockStarts']

    with open(output_file, 'w') as ofile:
        ofile.write(f"track name=\"{os.path.basename(output_file).replace('.bed12', '')}\" itemRgb=On\n")
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
            "light": "#EED8C9",
            "dark": "#C94A3F"
        },
        "condition2": {
            "light": "#D4E6F1",
            "dark": "#1D4F72"
        }
    }

    light_rgb = hex_to_rgb_tuple(BASE_COLORS[args.day]["light"])
    dark_rgb = hex_to_rgb_tuple(BASE_COLORS[args.day]["dark"])
    pb_to_ens, pb_to_category = load_sqanti_data(args.sqanti)
    add_rgb_colors(args.input_bed, light_rgb, dark_rgb, args.output_file, pb_to_ens, pb_to_category)

if __name__ == "__main__":
    main()