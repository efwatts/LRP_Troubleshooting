#!/usr/bin/env python3

import pandas as pd
import math
import argparse
from typing import Tuple, Union

# examine all pb transcripts of a gene, determine rgb color
def calculate_rgb_shading(grp: pd.DataFrame) -> pd.DataFrame:
    """
    Examine CPM for all PB transcripts of a gene and get RGB shading factor.
    """

    # rgb scaling
    rgb_scale = [
        '0,0,0', '26,0,0', '51,0,0', '77,0,0', '102,0,0',
        '128,0,0', '153,0,0', '179,0,0', '204,0,0', '230,0,0',
        '255,0,0', '255,26,26', '255,51,51', '255,77,77', '255,102,102',
        '255,128,128', '255,153,153', '255,179,179', '255,204,204', '255,230,230'
    ]
    max_cpm = grp.cpm.max()
    out_rows = []

    for _, row in grp.iterrows():
        cpm = row['cpm']
        if cpm > 0:
            fc = float(max_cpm) / float(cpm)
            log2fc = math.log(fc, 2)
            log2fcx3 = log2fc * 3
            ceil_idx = min(math.ceil(log2fcx3), 19)
            rgb = rgb_scale[ceil_idx]
        else:
            fc = 0
            log2fc = 0
            log2fcx3 = 0
            ceil_idx = 19
            rgb = rgb_scale[-1]

        out_rows.append({
            'acc_full': row['acc_full'],
            'pb_acc': row['pb_acc'],
            'cpm': row['cpm'],
            'fc': fc,
            'log2fc': log2fc,
            'log2fcx3': log2fcx3,
            'ceil_idx': ceil_idx,
            'rgb': rgb
        })

    out_df = pd.DataFrame(out_rows)
    out_df = out_df[['acc_full', 'rgb']]
    return out_df


def add_rgb_shading_cpm(name: str, bed: pd.DataFrame, split_size: int) -> None:
    """
    Reads a BAM file containing CPM info to determine rgb color to use for track visualization

    Parameters
    ----------
    name : str 
        name of sample
    bed : pd.DataFrame
        dataframe of bed cds to read
    split_size : int
        number of split elements in acc_full
    """

    if split_size == 3:
        subbed = bed[['acc_full', 'gene', 'pb_acc', 'cpm']].copy()
    elif split_size == 4:
        subbed = bed[['acc_full', 'gene', 'pb_acc', 'pclass', 'cpm']].copy()
    subbed['cpm'] = subbed['cpm'].astype(float).astype(int)

    shaded = subbed.groupby('gene').apply(calculate_rgb_shading).reset_index(drop=True)

    bed_shaded = pd.merge(bed, shaded, how='left', on='acc_full')
    bed_shaded.gene = bed_shaded.gene.apply(lambda x: x[:9])

    bed_shaded['cpm'] = bed_shaded['cpm'].apply(lambda cpm: str(cpm) if int(cpm) <= 1000 else f'{int(cpm) / 1000:.1f}K')

    if split_size == 3:
        bed_shaded['new_acc_full'] = bed_shaded['acc_full']
    elif split_size == 4:
        bed_shaded['new_acc_full'] = bed_shaded['acc_full']

    bed_shaded = bed_shaded[['chrom', 'chromStart', 'chromStop', 'new_acc_full', 'score', 'strand', 'thickStart', 'thickEnd', 'rgb', 'blockCount', 'blockSizes', 'blockStarts']]

    with open(f'{name}_shaded_cpm.bed12', 'w') as ofile:
        ofile.write(f'track name="{name.capitalize()} PacBio Protein" itemRgb=On\n')
        bed_shaded.to_csv(ofile, sep='\t', index=False, header=False)


def add_rgb_shading_pclass(name: str, bed: pd.DataFrame) -> None:
    pclass_shading_dict = {
        'pFSM': '100,165,200',
        'pNIC': '111,189,113',
        'pNNC': '232,98,76',
        'pISM': '248,132,85'
    }
    bed['rgb'] = bed['pclass'].map(pclass_shading_dict).fillna('0,0,0')

    bed.gene = bed.gene.apply(lambda x: x[:9])

    bed['cpm'] = bed['cpm'].apply(lambda cpm: str(cpm) if int(cpm) <= 1000 else f'{int(cpm) / 1000:.1f}K')

    bed['new_acc_full'] = bed['acc_full']

    filter_names = ['chrom', 'chromStart', 'chromStop', 'new_acc_full', 'score', 'strand', 'thickStart', 'thickEnd', 'rgb', 'blockCount', 'blockSizes', 'blockStarts']
    bed = bed[filter_names]
    with open(f'{name}_shaded_protein_class.bed12', 'w') as ofile:
        ofile.write(f'track name="{name.capitalize()} PacBio Protein" itemRgb=On\n')
        bed.to_csv(ofile, sep='\t', index=False, header=False)


def add_rgb_shading(name: str, bed_file: str) -> None:
    bed_names = ['chrom', 'chromStart', 'chromStop', 'acc_full', 'score', 'strand', 'thickStart', 'thickEnd', 'itemRGB', 'blockCount', 'blockSizes', 'blockStarts']
    bed = pd.read_table(bed_file, names=bed_names)
    split_size = len(bed.loc[0, 'acc_full'].split('|'))

    if split_size == 3:
        bed[['gene', 'pb_acc', 'cpm']] = bed['acc_full'].str.split('|', expand=True)
    elif split_size == 4:
        bed[['gene', 'pb_acc', 'pclass', 'cpm']] = bed['acc_full'].str.split('|', expand=True)
    bed = bed[bed.gene != '-']

    add_rgb_shading_cpm(name, bed.copy(), split_size)
    if split_size == 4:
        add_rgb_shading_pclass(name, bed)


def main() -> None:
    parser = argparse.ArgumentParser(description="IO file locations for making region bed")
    parser.add_argument("--name", required=True, help="name of sample - used for output file name")
    parser.add_argument("--bed_file", required=True, help="sample bed with cds")
    args = parser.parse_args()
    add_rgb_shading(args.name, args.bed_file)


if __name__ == "__main__":
    main()
