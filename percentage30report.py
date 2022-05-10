'''
Script to generate report of sub-optimally covered genes from Sambamba output

Author: Chris Pyatt
'''

# import libraries
import argparse
import pandas as pd
import re
import sys


def get_args():
    '''
    Parses command line arguments. Returns the arguments as strings.
    '''
    parser = argparse.ArgumentParser(
    
    )
    parser.add_argument(
        '--file',
        help='sambamba output file (input to this script)'
    )
    parser.add_argument(
        '--verbose',action='store_true',
        help='if enabled, reports more info about the gene(s) with sub-optimal coverage'
    )
    parser.add_argument(
        '--output',
        help='name of %%30 coverage report'
    )
    parser.add_argument(
        '--threshold',nargs='?',default='100',
        help='coverage threshold under which to report. NB. threshold applied at exon level'
    )
    args = parser.parse_args()
    # exit gracefully if no arguments given (or missing either file or output)
    if args.file == None or args.output == None:
        parser.print_help()
        sys.exit(1)
    else:
        return args


def get_input(args):
    '''
    Reads input file and makes into pandas dataframe.
    '''
    with open(args.file) as file:
        # separator argument negates mix of tabs and spaces
        df = pd.read_csv(file, sep=r"\s+")
    return df


def find_subopt(data, threshold):
    '''
    Takes an input dataframe & a coverage threshold. Returns a subset of rows where the value of 'percentage30' is lower than the threshold. Input must have (minimum) columns as below.
    '''
    try:
        trimColumns = data[["FullPosition", "GeneSymbol;Accession", "readCount", "meanCoverage", "percentage30"]]
    except:
        print('Required columns not found - is the input file in the correct format?')
        sys.exit(1)
    subopt = trimColumns.loc[trimColumns['percentage30'] < float(threshold)]
    return subopt
    
    
def make_output(data, verbose):
    '''
    Takes suboptimal coverage dataframe & converts to output list. Output content depends on whether verbose option is enabled.
    '''
    geneDf = data[["GeneSymbol;Accession"]].drop_duplicates("GeneSymbol;Accession")
    uniqueGenes = geneDf["GeneSymbol;Accession"].values.tolist()
    if verbose:
        out = []
        for i in uniqueGenes:
            gene = i.split(';')[0]
            out.append(gene)
            # more readable headers
            out.append('Exon_Genomic_Position\tGene_Transcript\tRead_Count\tMean_Coverage\tPercentage_>=30X')
            # exon output for gene
            data_string = data.loc[data['GeneSymbol;Accession'] == i].to_string(index=False,header=False)
            # replaces (multiple) spaces with tabs
            data_string_tabbed = re.sub(' +', '\t', data_string)
            out.append(data_string_tabbed)
            out.append('\n')
    else:
        out = []
        for i in uniqueGenes:
            gene = i.split(';')[0]
            out.append(gene)
    return out


def write_output(args,data):
    '''
    Writes output to a file. Takes args to get output filename and data = a list of genes (& other info if verbose enabled).
    '''
    with open(args.output,'w') as outfile:
        outfile.write("The genes listed below have suboptimal coverage in at least one exon:\n\n")    
        for line in data:
            outfile.write(line)
            outfile.write("\n")


def main():
    args = get_args()
    inp = get_input(args)
    sub = find_subopt(inp,args.threshold)
    if args.verbose:
        out = make_output(sub, True)
    else:
        out = make_output(sub, False)
    write_output(args,out)    
    

if __name__ == "__main__":
    main()
