#!/usr/bin/env python3

import pandas as pd
import argparse
import os

# Pink-to-black color scale (reversed so high PSI = black)
rgb_scale = list(reversed([
    '0,0,0', '26,0,0', '51,0,0', '77,0,0', '102,0,0',
    '128,0,0', '153,0,0', '179,0,0', '204,0,0', '230,0,0',
    '255,0,0', '255,26,26', '255,51,51', '255,77,77', '255,102,102',
    '255,128,128', '255,153,153', '255,179,179', '255,204,204', '255,230,230'
]))

def psi_to_rgb(psi):
    if pd.isna(psi) or psi is None:
        return '128,128,128'
    psi = max(0, min(1, psi))
    idx = min(int(psi * (len(rgb_scale) - 1)), len(rgb_scale) - 1)
    return rgb_scale[idx]

def extract_mean_psi(psi_str):
    values = [float(x) for x in psi_str.split(",") if x not in ("NA", "")]
    return round(sum(values)/len(values), 3) if values else 0.0

def get_event_coordinates(row, event_type):
    """Extract coordinates based on event type"""
    coords = {
        'chr': row['chr'],
        'strand': row['strand']
    }
    
    if event_type in ['SE', 'MXE', 'RI']:
        # These event types have upstream/downstream coordinates
        coords['upstream_start'] = int(row['upstreamES'])
        coords['upstream_end'] = int(row['upstreamEE'])
        coords['downstream_start'] = int(row['downstreamES'])
        coords['downstream_end'] = int(row['downstreamEE'])
    
    if event_type == 'SE':
        coords['exon_start'] = int(row['exonStart_0base'])
        coords['exon_end'] = int(row['exonEnd'])
    elif event_type == 'MXE':
        coords['exon1_start'] = int(row['1stExonStart_0base'])
        coords['exon1_end'] = int(row['1stExonEnd'])
        coords['exon2_start'] = int(row['2ndExonStart_0base'])
        coords['exon2_end'] = int(row['2ndExonEnd'])
    elif event_type in ['A3SS', 'A5SS']:
        # A3SS/A5SS use flanking exon instead of upstream/downstream
        coords['long_start'] = int(row['longExonStart_0base'])
        coords['long_end'] = int(row['longExonEnd'])
        coords['short_start'] = int(row['shortES'])
        coords['short_end'] = int(row['shortEE'])
        coords['flanking_start'] = int(row['flankingES'])
        coords['flanking_end'] = int(row['flankingEE'])
    elif event_type == 'RI':
        coords['ri_start'] = int(row['riExonStart_0base'])
        coords['ri_end'] = int(row['riExonEnd'])
    
    return coords

def construct_bed12_se(coords, psi, psi_alt, event_id, strand, sig_marker="", flank_length=100, full_exon_flanks=False):
    """Construct BED12 entries for SE events"""
    chrom = coords['chr']
    
    if full_exon_flanks:
        upstream_start = coords['upstream_start']
        upstream_end = coords['upstream_end']
        downstream_start = coords['downstream_start']
        downstream_end = coords['downstream_end']
    else:
        upstream_end = coords['upstream_end']
        upstream_start = max(0, upstream_end - flank_length)
        downstream_start = coords['downstream_start']
        downstream_end = downstream_start + flank_length

    exon_start = coords['exon_start']
    exon_end = coords['exon_end']

    rgb = psi_to_rgb(psi)
    rgb_alt = psi_to_rgb(psi_alt)

    # Inclusion isoform (3 blocks)
    blocks_inc = [upstream_end - upstream_start, exon_end - exon_start, downstream_end - downstream_start]
    rel_starts_inc = [0, exon_start - upstream_start, downstream_start - upstream_start]
    bed_inc = [
        chrom, str(upstream_start), str(downstream_end),
        f"{event_id}:inclusion|{psi:.3f}{sig_marker}", "0", strand,
        str(downstream_end), str(downstream_end), rgb, "3",
        ",".join(map(str, blocks_inc)) + ",",
        ",".join(map(str, rel_starts_inc)) + ","
    ]

    # Skipping isoform (2 blocks)
    blocks_exc = [upstream_end - upstream_start, downstream_end - downstream_start]
    rel_starts_exc = [0, downstream_start - upstream_start]
    bed_exc = [
        chrom, str(upstream_start), str(downstream_end),
        f"{event_id}:skipping|{psi_alt:.3f}{sig_marker}", "0", strand,
        str(downstream_end), str(downstream_end), rgb_alt, "2",
        ",".join(map(str, blocks_exc)) + ",",
        ",".join(map(str, rel_starts_exc)) + ","
    ]

    return bed_inc, bed_exc

def construct_bed12_mxe(coords, psi, psi_alt, event_id, strand, sig_marker="", flank_length=100, full_exon_flanks=False):
    """Construct BED12 entries for MXE events"""
    chrom = coords['chr']
    
    if full_exon_flanks:
        upstream_start = coords['upstream_start']
        upstream_end = coords['upstream_end']
        downstream_start = coords['downstream_start']
        downstream_end = coords['downstream_end']
    else:
        upstream_end = coords['upstream_end']
        upstream_start = max(0, upstream_end - flank_length)
        downstream_start = coords['downstream_start']
        downstream_end = downstream_start + flank_length

    exon1_start = coords['exon1_start']
    exon1_end = coords['exon1_end']
    exon2_start = coords['exon2_start']
    exon2_end = coords['exon2_end']

    rgb = psi_to_rgb(psi)
    rgb_alt = psi_to_rgb(psi_alt)

    # First exon isoform (3 blocks)
    blocks_1st = [upstream_end - upstream_start, exon1_end - exon1_start, downstream_end - downstream_start]
    rel_starts_1st = [0, exon1_start - upstream_start, downstream_start - upstream_start]
    bed_1st = [
        chrom, str(upstream_start), str(downstream_end),
        f"{event_id}:exon1|{psi:.3f}{sig_marker}", "0", strand,
        str(downstream_end), str(downstream_end), rgb, "3",
        ",".join(map(str, blocks_1st)) + ",",
        ",".join(map(str, rel_starts_1st)) + ","
    ]

    # Second exon isoform (3 blocks)
    blocks_2nd = [upstream_end - upstream_start, exon2_end - exon2_start, downstream_end - downstream_start]
    rel_starts_2nd = [0, exon2_start - upstream_start, downstream_start - upstream_start]
    bed_2nd = [
        chrom, str(upstream_start), str(downstream_end),
        f"{event_id}:exon2|{psi_alt:.3f}{sig_marker}", "0", strand,
        str(downstream_end), str(downstream_end), rgb_alt, "3",
        ",".join(map(str, blocks_2nd)) + ",",
        ",".join(map(str, rel_starts_2nd)) + ","
    ]

    return bed_1st, bed_2nd

def construct_bed12_a3ss_a5ss(coords, psi, psi_alt, event_id, strand, sig_marker="", flank_length=100, full_exon_flanks=False, event_type='A3SS'):
    """Construct BED12 entries for A3SS/A5SS events"""
    chrom = coords['chr']
    
    long_start = coords['long_start']
    long_end = coords['long_end']
    short_start = coords['short_start']
    short_end = coords['short_end']
    flanking_start = coords['flanking_start']
    flanking_end = coords['flanking_end']

    rgb = psi_to_rgb(psi)
    rgb_alt = psi_to_rgb(psi_alt)

    # For A3SS/A5SS, the structure is simpler:
    # We have the long exon, short exon, and flanking exon
    # Need to create 2-block entries showing the alternative splice sites
    
    # Determine the overall region boundaries
    all_starts = [long_start, short_start, flanking_start]
    all_ends = [long_end, short_end, flanking_end]
    region_start = min(all_starts)
    region_end = max(all_ends)

    # Long isoform: long exon + flanking exon
    if long_start < flanking_start:
        # Long exon comes first
        blocks_long = [long_end - long_start, flanking_end - flanking_start]
        rel_starts_long = [long_start - region_start, flanking_start - region_start]
    else:
        # Flanking exon comes first
        blocks_long = [flanking_end - flanking_start, long_end - long_start]
        rel_starts_long = [flanking_start - region_start, long_start - region_start]

    bed_long = [
        chrom, str(region_start), str(region_end),
        f"{event_id}:long|{psi:.3f}{sig_marker}", "0", strand,
        str(region_end), str(region_end), rgb, "2",
        ",".join(map(str, blocks_long)) + ",",
        ",".join(map(str, rel_starts_long)) + ","
    ]

    # Short isoform: short exon + flanking exon
    if short_start < flanking_start:
        # Short exon comes first
        blocks_short = [short_end - short_start, flanking_end - flanking_start]
        rel_starts_short = [short_start - region_start, flanking_start - region_start]
    else:
        # Flanking exon comes first
        blocks_short = [flanking_end - flanking_start, short_end - short_start]
        rel_starts_short = [flanking_start - region_start, short_start - region_start]

    bed_short = [
        chrom, str(region_start), str(region_end),
        f"{event_id}:short|{psi_alt:.3f}{sig_marker}", "0", strand,
        str(region_end), str(region_end), rgb_alt, "2",
        ",".join(map(str, blocks_short)) + ",",
        ",".join(map(str, rel_starts_short)) + ","
    ]

    return bed_long, bed_short

def construct_bed12_ri(coords, psi, psi_alt, event_id, strand, sig_marker="", flank_length=100, full_exon_flanks=False):
    """Construct BED12 entries for RI events"""
    chrom = coords['chr']
    
    if full_exon_flanks:
        upstream_start = coords['upstream_start']
        upstream_end = coords['upstream_end']
        downstream_start = coords['downstream_start']
        downstream_end = coords['downstream_end']
    else:
        upstream_end = coords['upstream_end']
        upstream_start = max(0, upstream_end - flank_length)
        downstream_start = coords['downstream_start']
        downstream_end = downstream_start + flank_length

    ri_start = coords['ri_start']
    ri_end = coords['ri_end']

    rgb = psi_to_rgb(psi)
    rgb_alt = psi_to_rgb(psi_alt)

    # Retention isoform (1 block - continuous)
    bed_retention = [
        chrom, str(upstream_start), str(downstream_end),
        f"{event_id}:retention|{psi:.3f}{sig_marker}", "0", strand,
        str(downstream_end), str(downstream_end), rgb, "1",
        str(downstream_end - upstream_start) + ",",
        "0,"
    ]

    # Splicing isoform (2 blocks)
    blocks_splice = [upstream_end - upstream_start, downstream_end - downstream_start]
    rel_starts_splice = [0, downstream_start - upstream_start]
    bed_splice = [
        chrom, str(upstream_start), str(downstream_end),
        f"{event_id}:splicing|{psi_alt:.3f}{sig_marker}", "0", strand,
        str(downstream_end), str(downstream_end), rgb_alt, "2",
        ",".join(map(str, blocks_splice)) + ",",
        ",".join(map(str, rel_starts_splice)) + ","
    ]

    return bed_retention, bed_splice

def detect_event_type(df):
    """Auto-detect event type based on column names"""
    columns = set(df.columns)
    
    if 'exonStart_0base' in columns and 'exonEnd' in columns:
        return 'SE'
    elif '1stExonStart_0base' in columns and '2ndExonStart_0base' in columns:
        return 'MXE'
    elif 'longExonStart_0base' in columns and 'shortES' in columns and 'flankingES' in columns:
        # Distinguish A3SS from A5SS based on filename or user input
        return 'A3SS'  # Default, can be overridden by command line
    elif 'riExonStart_0base' in columns:
        return 'RI'
    else:
        raise ValueError("Cannot detect event type from column names")

def main():
    parser = argparse.ArgumentParser(description="Convert rMATS output to SUPPA-style BED12 format")
    parser.add_argument("--input", required=True, help="Path to rMATS output file")
    parser.add_argument("--output1", required=True, help="Output BED12 for condition 1")
    parser.add_argument("--output2", required=True, help="Output BED12 for condition 2")
    parser.add_argument("--event_type", choices=['SE', 'MXE', 'A3SS', 'A5SS', 'RI'], 
                       help="Event type (auto-detected if not specified)")
    parser.add_argument("--track_name1", help="Track name for condition 1 (auto-generated if not specified)")
    parser.add_argument("--track_name2", help="Track name for condition 2 (auto-generated if not specified)")
    parser.add_argument("--flank_length", type=int, default=100, help="Fixed exon flank length")
    parser.add_argument("--full_exon_flanks", action="store_true", help="Use full exon lengths for flanks")
    args = parser.parse_args()

    df = pd.read_csv(args.input, sep="\t")
    
    # Auto-detect event type if not specified
    if args.event_type is None:
        event_type = detect_event_type(df)
        print(f"Auto-detected event type: {event_type}")
    else:
        event_type = args.event_type

    # Set default track names if not provided
    if args.track_name1 is None:
        args.track_name1 = f"{event_type}_Cond1"
    if args.track_name2 is None:
        args.track_name2 = f"{event_type}_Cond2"

    # Assign unique event IDs per gene
    df["geneSymbol"] = df["geneSymbol"].fillna("NA")
    df["geneSymbol"] = df["geneSymbol"].str.replace("[^a-zA-Z0-9]", "_", regex=True)
    
    # Sort by appropriate coordinates based on event type
    if event_type == 'SE':
        df = df.sort_values(["geneSymbol", "exonStart_0base", "exonEnd"])
    elif event_type == 'MXE':
        df = df.sort_values(["geneSymbol", "1stExonStart_0base", "1stExonEnd"])
    elif event_type in ['A3SS', 'A5SS']:
        df = df.sort_values(["geneSymbol", "longExonStart_0base", "longExonEnd"])
    elif event_type == 'RI':
        df = df.sort_values(["geneSymbol", "riExonStart_0base", "riExonEnd"])
    
    df["event_id"] = df.groupby("geneSymbol").cumcount() + 1
    df["event_id"] = f"{event_type}_" + df["geneSymbol"] + "_" + df["event_id"].astype(str)

    bed1_lines = [f"track name={args.track_name1} description=\"{args.track_name1}\" itemRgb=On"]
    bed2_lines = [f"track name={args.track_name2} description=\"{args.track_name2}\" itemRgb=On"]

    for _, row in df.iterrows():
        sig_marker = "*" if row.get("PValue", 1.0) < 0.05 else ""
        psi1 = extract_mean_psi(row["IncLevel1"])
        psi2 = extract_mean_psi(row["IncLevel2"])
        event_id = row["event_id"]
        
        coords = get_event_coordinates(row, event_type)
        
        # Construct BED12 entries based on event type
        if event_type == 'SE':
            bed1a, bed1b = construct_bed12_se(coords, psi1, 1 - psi1, event_id, row["strand"], 
                                            sig_marker, args.flank_length, args.full_exon_flanks)
            bed2a, bed2b = construct_bed12_se(coords, psi2, 1 - psi2, event_id, row["strand"], 
                                            sig_marker, args.flank_length, args.full_exon_flanks)
        elif event_type == 'MXE':
            bed1a, bed1b = construct_bed12_mxe(coords, psi1, 1 - psi1, event_id, row["strand"], 
                                             sig_marker, args.flank_length, args.full_exon_flanks)
            bed2a, bed2b = construct_bed12_mxe(coords, psi2, 1 - psi2, event_id, row["strand"], 
                                             sig_marker, args.flank_length, args.full_exon_flanks)
        elif event_type in ['A3SS', 'A5SS']:
            bed1a, bed1b = construct_bed12_a3ss_a5ss(coords, psi1, 1 - psi1, event_id, row["strand"], 
                                                   sig_marker, args.flank_length, args.full_exon_flanks, event_type)
            bed2a, bed2b = construct_bed12_a3ss_a5ss(coords, psi2, 1 - psi2, event_id, row["strand"], 
                                                   sig_marker, args.flank_length, args.full_exon_flanks, event_type)
        elif event_type == 'RI':
            bed1a, bed1b = construct_bed12_ri(coords, psi1, 1 - psi1, event_id, row["strand"], 
                                            sig_marker, args.flank_length, args.full_exon_flanks)
            bed2a, bed2b = construct_bed12_ri(coords, psi2, 1 - psi2, event_id, row["strand"], 
                                            sig_marker, args.flank_length, args.full_exon_flanks)

        bed1_lines.append("\t".join(bed1a))
        bed1_lines.append("\t".join(bed1b))
        bed2_lines.append("\t".join(bed2a))
        bed2_lines.append("\t".join(bed2b))

    with open(args.output1, "w") as f1:
        f1.write("\n".join(bed1_lines) + "\n")
    with open(args.output2, "w") as f2:
        f2.write("\n".join(bed2_lines) + "\n")

    print(f"Processed {len(df)} {event_type} events")
    print(f"Output written to {args.output1} and {args.output2}")

if __name__ == "__main__":
    main()