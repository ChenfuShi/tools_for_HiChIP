## Author: Chenfu Shi
## Last update date: 14/11/2018
## Contact: chenfu.shi@postgrad.manchster.ac.uk
## This software is distributed without any guarantee on it's functionality

# hichipper output for washu doesn't use the FDR values. 
# I'm taking the all.mango output files and making fresh washu files


import argparse


parser = argparse.ArgumentParser(description='convert hichipper mango output to washu pairwise interaction files with FDR scores')

parser.add_argument("-i",'--input', dest='inputfile', action='store', required=True,
                    help='input file name (interactions.all.mango file)')
parser.add_argument("-o",'--output', dest='outputfile', action='store', required=False,
                    help='ouput file name')
parser.add_argument('-f', action='store_true', dest='filter', help='filter for FDR < 0.10')

args = parser.parse_args()

if args.outputfile:
    outputname=args.ouputfile
else:
    outputname=args.inputfile + ".washu.txt"

with open(outputname, "w") as outputfile, open(args.inputfile , "r") as inputfile:
    for line in inputfile:
        data = line.split("\t")
        if filter and float(data[7].strip()) > 0.10:
            continue
        outputfile.write("{},{},{}\t{},{},{}\t{}\n".format(data[0],data[1],data[2],data[3],data[4],data[5],str(1-float(data[7].strip()))))

