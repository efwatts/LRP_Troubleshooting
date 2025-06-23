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
    '255,128,128', '255,153,153', '255,179,179', '255,204,204', '255,230,230'
]

# Fixed RGB for class-based visualization
pclass_shading_dict = {
    'pFSM': '100,165,200',
    'pNIC': '111,189,113',
    'pNNC': '232,98,76',
    'pISM': '248,132,85'
}

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

def extract_fields(acc):
    parts = acc.split('|')
    if len(parts) < 4:
        return pd.Series([None]*5)
    gene, tx_id, cpm, frac = parts[0], parts[1], parts[2], parts[3]
    is_novel = acc.endswith("*")
    return pd.Series([gene, tx_id, float(cpm), float(frac.rstrip("*")), is_novel])

def add_rgb_colors(input_bed, output_file):
    bed_names = ['chrom','chromStart','chromStop','acc_full','score','strand',
                 'thickStart','thickEnd','itemRGB','blockCount','blockSizes','blockStarts']
    bed = pd.read_table(input_bed, names=bed_names, comment='#')

    bed[['gene', 'tx_id', 'cpm', 'frac', 'is_novel']] = bed['acc_full'].astype(str).apply(extract_fields)
    bed = bed.dropna(subset=['gene', 'tx_id', 'cpm', 'frac'])

    bed['gene_total_cpm'] = bed.groupby('gene')['cpm'].transform('sum')
    bed = bed[bed['gene_total_cpm'] > 0]

    # Optional: parse class from transcript ID if embedded (e.g., PBID contains class info)
    bed['pclass'] = bed['tx_id'].apply(lambda tid: tid.split('.')[0] if tid.startswith('p') else None)

    # Calculate RGB shading per gene
    shaded = bed.groupby('gene').apply(calculate_rgb_shading).reset_index(drop=True)
    bed = pd.merge(bed, shaded, on='acc_full', how='left')

    # Override RGB with class-based shading if applicable
    bed['rgb'] = bed.apply(lambda row: pclass_shading_dict.get(row['pclass'], row['rgb']), axis=1)

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
    parser.add_argument("--input_bed", required=True, help="Input BED12 file with acc_full in format Gene|TranscriptID|CPM|Frac[*]")
    parser.add_argument("--output_file", required=True, help="Output BED12 file")
    args = parser.parse_args()

    add_rgb_colors(args.input_bed, args.output_file)

if __name__ == "__main__":
    main()