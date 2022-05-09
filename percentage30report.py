# import libraries
import argparse
import pandas as pd

# define arg parser
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
        help='if enabled, reports more info about the gene with sub-optimal coverage'
    )
    parser.add_argument(
        '--output',
        help='name of %30 coverage report'
    )
    args = parser.parse_args()
    return args



# read in input file as dataframe
def get_input(args):
    with open(args.file) as file:
        df = pd.read_csv(file, sep=r"\s+")
    return df


# loop thru input file
# if percentage30 is not 100, make note of gene
def find_subopt(data):
    trimColumns = data[["FullPosition", "GeneSymbol;Accession", "readCount", "meanCoverage", "percentage30"]]
    subopt = trimColumns.loc[trimColumns['percentage30'] < 100]
    return subopt
    
    
def make_verbose_output(data):
    pass


# write list of offending genes to file
def write_output(args,data):
    with open(args.output,'w') as outfile:
        outfile.write("The genes listed below have suboptimal coverage in at least one exon:\n")    
        for line in data:
            outfile.write(line)
            outfile.write("\n")
    print(data)


def main():
    args = get_args()
    inp = get_input(args)
    sub = find_subopt(inp)
    if args.verbose:
        pass
    else:
        geneDf = sub[["GeneSymbol;Accession"]].drop_duplicates("GeneSymbol;Accession")
        out = (geneDf["GeneSymbol;Accession"].values.tolist())
    write_output(args,out)    
    

if __name__ == "__main__":
    main()
