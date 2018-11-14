## Author: Chenfu Shi
## Last update date: 14/11/2018
## Contact: chenfu.shi@postgrad.manchster.ac.uk
## This software is distributed without any guarantee on it's functionality

# hichipper output for washu doesn't use the FDR values. 
# I'm taking the all.mango output files and making fresh washu files


import argparse
import gzip

parser = argparse.ArgumentParser(description='convert hichipper mango output to washu gz compressed pairwise interaction files with FDR scores')

parser.add_argument("-i",'--input', dest='inputfile', action='store', required=True,
                    help='input file name (interactions.all.mango file)')
parser.add_argument("-o",'--output', dest='outputfile', action='store', required=False,
                    help='ouput file name (gz compressed file)')

args = parser.parse_args()

if args.outputfile:
    outputname=args.ouputfile
else:
    outputname=args.inputfile + "washu.gz"

with gzip.open(outputname, "wt", compresslevel=5) as outputfile, open(args.inputfile , "r") as inputfile:
    for line in inputfile:
        data = line.split("\t")

        outputfile.write("{},{},{}\t{},{},{}\t{}".format(data[0],data[1],data[2],data[3],data[4],data[5],str(1-int(data[7].strip()))))

