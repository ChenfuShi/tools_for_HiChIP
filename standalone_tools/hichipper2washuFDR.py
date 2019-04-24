## Author: Chenfu Shi
## Last update date: 14/11/2018
## Contact: chenfu.shi@postgrad.manchster.ac.uk
## This software is distributed without any guarantee on it's functionality

# hichipper output for washu doesn't use the FDR values. 
# I'm taking the all.mango output files and making fresh washu files
# updated for use in new washu format
# will use gbzip and tabix to compress and index everything!
# FDR score is reversed because otherwise very good values would be very low for washu scoring

import argparse


parser = argparse.ArgumentParser(description='convert hichipper mango output to washu pairwise interaction files with FDR scores')

parser.add_argument("-i",'--input', dest='inputfile', action='store', required=True,
                    help='input file name (interactions.all.mango file)')
parser.add_argument("-o",'--output', dest='outputfile', action='store', required=False,
                    help='ouput file name')

parser.add_argument('-f', '--filter' , dest='filter', action='store', type=float, default=0.10, required=False,
                    help='filter FDR threshold (<)')

parser.add_argument('-v', '--old_washu' ,action='store_true', dest='old', help='use old washu format')

parser.add_argument("-t",'--threshold', dest='threshold', action='store', type=int, default=1, required=False,
                    help='minimum read for interaction threshold (>)')

args = parser.parse_args()

if args.outputfile:
    outputname=args.outputfile
else:
    outputname=args.inputfile + ".washu.txt"
FDR_thres = args.filter
Old_washu = args.old
ID_counter = 1

with open(outputname, "w") as outputfile, open(args.inputfile , "r") as inputfile:
    for line in inputfile:
        data = line.split("\t")
        if float(data[7].strip()) > FDR_thres:
            # do nothing if FDR value is above FDR
            continue
        if args.threshold < int(data[6]):
            # filter for threshold of read count
            if Old_washu:
                outputfile.write("{},{},{}\t{},{},{}\t{}\n".format(data[0],data[1],data[2],data[3],data[4],data[5],str(1-float(data[7].strip()))))
            else:
                outputfile.write("{}\t{}\t{}\t{}:{}-{},{}\t{}\t{}\n".format(data[0],data[1],data[2],data[3],data[4],data[5],str(1-float(data[7].strip())),str(ID_counter),"."))
                ID_counter = ID_counter + 1
                outputfile.write("{}\t{}\t{}\t{}:{}-{},{}\t{}\t{}\n".format(data[3],data[4],data[5],data[0],data[1],data[2],str(1-float(data[7].strip())),str(ID_counter),"."))
                ID_counter = ID_counter + 1


if not Old_washu:
    import subprocess
    subprocess.run(["bgzip",outputname])
    subprocess.run(["tabix","-p","bed",outputname+"gz"])