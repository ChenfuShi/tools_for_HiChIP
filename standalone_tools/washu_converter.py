## Author: Chenfu Shi
## Last update date: 24/04/2019
## Contact: chenfu.shi@postgrad.manchster.ac.uk
## This software is distributed without any guarantee on it's functionality



# converts the old washu interactions format to the new one
import argparse
import subprocess

parser = argparse.ArgumentParser(description='converts the old washu interactions format to the new one')




parser.add_argument("-i",'--input', dest='inputfile', action='store', required=True,
                    help='input file name (interactions.all.mango file)')
parser.add_argument("-o",'--output', dest='outputfile', action='store', required=False,
                    help='ouput file name')


args = parser.parse_args()

if args.outputfile:
    outputname=args.outputfile
else:
    outputname=args.inputfile + ".new_washu.bed"

ID_counter = 1


with open(outputname, "w") as outputfile, open(args.inputfile , "r") as inputfile:
    for line in inputfile:
        data = line.split("\t")
        start = data[0].split(",")
        end = data[1].split(",")
        score = data[2].strip()
        outputfile.write("{}\t{}\t{}\t{}:{}-{},{}\t{}\t{}\n".format(start[0],start[1],start[2],end[0],end[1],end[2],score,1,"."))
        ID_counter = ID_counter + 1
        outputfile.write("{}\t{}\t{}\t{}:{}-{},{}\t{}\t{}\n".format(end[0],end[1],end[2],start[0],start[1],start[2],score,1,"."))
        ID_counter = ID_counter + 1
        


subprocess.run(["sort","-o",outputname,"-k1,1","-k2,2n",outputname])
subprocess.run(["bgzip",outputname])
subprocess.run(["tabix","-p","bed",outputname+".gz"])