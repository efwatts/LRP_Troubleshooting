#!/usr/bin/env python3

import pandas as pd
import argparse
import os
import math

# Coarse red-scale RGB gradient for relative abundance
rgb_scale = [
    '0,0,0', '26,0,0', '51,0,0', '77,0,0', '102,0,0',
    '128,0,0', '153,0,0', '179,0,0', '204,0,0', '230,0,0',
    '255,0,0', '255,26,26', '255,51,51', '255,77,77', '255,102,102',
    '255,128,128', '255,153,153', '255,179,179', '255,204,204', '255,230,230']

# Fixed RGB for class-based visualization
pclass_shading_dict = {
    'pFSM': '100,165,200',
    'pNIC': '111,189,113',
    'pNNC': '232,98,76',
    'pISM': '248,132,85'
}

def load_pb_to_ens(sqanti_path):
    try:
        sqanti = pd.read_csv(sqanti_path, sep="\t")
        return sqanti.set_index("isoform")["associated_transcript"].to_dict()
    except Exception as e:
        print(f"Error loading SQANTI table: {e}")
        return {}

def replace_pb_with_ensembl(label, pb_to_ens, cpm_str, frac_str):
    try:
        gene, pb_id, *_ = label.split("|")
        enst = pb_to_ens.get(pb_id, pb_id)
        is_novel = (enst == "novel") or pd.isna(enst)
        if is_novel:
            return f"{gene}|{pb_id}|{cpm_str}|{frac_str}*"
        else:
            return f"{gene}|{enst}|{cpm_str}|{frac_str}"
    except Exception:
        return label

def calculate_rgb_shading(grp):
    max_cpm = grp.cpm.max()
    records = []
    for _, row in grp.iterrows():
        cpm = row['cpm']
        if cpm > 0:
            fc = float(max_cpm) / float(cpm)
            log2fc = math.log(fc, 2)
            ceil_idx = min(math.ceil(log2fc * 3), 19)
            rgb = rgb_scale[ceil_idx]
        else:
            rgb = rgb_scale[-1]
        records.append({'acc_full': row['acc_full'], 'rgb': rgb})
    return pd.DataFrame(records)

def add_rgb_colors(input_bed, output_file, pb_to_ens):
    bed_names = ['chrom','chromStart','chromStop','acc_full','score','strand',
                 'thickStart','thickEnd','itemRGB','blockCount','blockSizes','blockStarts']
    bed = pd.read_table(input_bed, names=bed_names, comment='#')

    # Split acc_full into fields
    def extract_fields(acc):
        parts = acc.split('|')
        if len(parts) != 4:
            return pd.Series([None]*4)
        return pd.Series([parts[0], parts[1], parts[2], float(parts[3])])

    bed[['gene', 'pb_acc', 'pclass', 'cpm']] = bed['acc_full'].astype(str).apply(extract_fields)
    bed = bed.dropna(subset=['gene', 'pb_acc', 'pclass', 'cpm'])

    bed['cpm'] = bed['cpm'].astype(float)
    bed['gene_total_cpm'] = bed.groupby('gene')['cpm'].transform('sum')
    bed = bed[bed['gene_total_cpm'] > 0]
    bed['frac'] = bed['cpm'] / bed['gene_total_cpm']

    bed['cpm_str'] = bed['cpm'].map(lambda x: f"{x:.2f}")
    bed['frac_str'] = bed['frac'].map(lambda x: f"{x:.2f}")

    # Calculate RGB shading per gene
    shaded = bed.groupby('gene').apply(calculate_rgb_shading).reset_index(drop=True)
    bed = pd.merge(bed, shaded, on='acc_full', how='left')

    # Override with class shading if known class
    bed['rgb'] = bed.apply(lambda row: pclass_shading_dict.get(row['pclass'], row['rgb']), axis=1)

    # Replace acc_full with renamed label
    bed['acc_full'] = bed.apply(
        lambda row: replace_pb_with_ensembl(f"{row['gene']}|{row['pb_acc']}|{row['pclass']}|{row['cpm']}",
                                            pb_to_ens, row['cpm_str'], row['frac_str']), axis=1)

    int_columns = ['chromStart', 'chromStop', 'score', 'thickStart', 'thickEnd', 'blockCount']
    bed[int_columns] = bed[int_columns].astype(int)
    bed['blockSizes'] = bed['blockSizes'].apply(lambda x: ','.join([str(int(float(i))) for i in str(x).split(',') if i]))
    bed['blockStarts'] = bed['blockStarts'].apply(lambda x: ','.join([str(int(float(i))) for i in str(x).split(',') if i]))

    filter_names = ['chrom', 'chromStart', 'chromStop', 'acc_full', 'score', 'strand',
                    'thickStart', 'thickEnd', 'rgb', 'blockCount', 'blockSizes', 'blockStarts']

    with open(output_file, 'w') as ofile:
        ofile.write(f'track name="{os.path.basename(output_file).replace(".bed12", "")}" itemRgb=On\n')
        bed[filter_names].to_csv(ofile, sep='\t', index=None, header=None)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_bed", required=True, help="Input BED12 file with acc_full field")
    parser.add_argument("--output_file", required=True, help="Output BED12 file")
    parser.add_argument("--sqanti", required=True, help="SQANTI classification table for PB → Ensembl mapping")
    args = parser.parse_args()

    pb_to_ens = load_pb_to_ens(args.sqanti)
    add_rgb_colors(args.input_bed, args.output_file, pb_to_ens)

if __name__ == "__main__":
    main()
