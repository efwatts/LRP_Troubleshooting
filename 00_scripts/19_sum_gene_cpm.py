import pandas as pd
import argparse

def sum_gene_cpm(input_file, sample_columns):
    """
    Read the isoform-level CPM data and sum up values for each gene
    """
    # Read the input file
    df = pd.read_csv(input_file, sep='\t')

    # Group by Gene and sum the CPM values
    gene_cpm = df.groupby('Gene')[sample_columns].sum().reset_index()

    # Round to 2 decimal places
    gene_cpm[sample_columns] = gene_cpm[sample_columns].round(2)

    return gene_cpm

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Sum CPM values by gene from isoform data.')
    
    parser.add_argument('-i', '--input',
                        required=True,
                        help='Path to input file (output from previous script)')
    
    parser.add_argument('-o', '--output',
                        required=True,
                        help='Path for output file')

    parser.add_argument('-s', '--samples',
                        required=True,
                        help='Comma-separated list of sample columns to include in summing, e.g. "Sample1,Sample2,Sample3"')

    return parser.parse_args()

def main():
    """Main function to process the file and generate output"""
    args = parse_arguments()
    
    # Split the sample list by comma and strip whitespace
    sample_columns = [s.strip() for s in args.samples.split(',')]
    
    try:
        print(f"Processing input file: {args.input}")
        gene_cpm = sum_gene_cpm(args.input, sample_columns)
        
        print(f"Saving gene-level CPM to: {args.output}")
        gene_cpm.to_csv(args.output, sep='\t', index=False)
        
        print("Gene-level CPM table generated successfully!")
        
    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e}")
        return 1
    except KeyError as e:
        print(f"Error: One or more specified sample columns were not found in the input file - {e}")
        return 1
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
