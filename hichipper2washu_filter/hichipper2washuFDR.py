#########################################
# Author: Chenfu Shi
# Email: chenfu.shi@postgrad.manchester.ac.uk
# BSD-3-Clause License
# Copyright 2019 Chenfu Shi
# All rights reserved.

# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


#########################################
# hichipper output for washu doesn't use the FDR values. 
# I'm taking the all.mango output files and making fresh washu files
# updated for use in new washu format
# will use gbzip and tabix to compress and index everything!
# FDR score is reversed because otherwise very good values would be very low for washu scoring
# you can also filter by number of reads supporting the interaction
# FDR score filtering is automatically applied. to disable run with -f 1

import argparse
import os

parser = argparse.ArgumentParser(description='Convert hichipper mango output to washu pairwise interaction files and filters with FDR scores and minimum number of reads. Uses bgzip and tabix to compress and index the file')

parser.add_argument("-i",'--input', dest='inputfile', action='store', required=True,
                    help='input file name (interactions.all.mango file)')
parser.add_argument("-o",'--output', dest='outputfile', action='store', required=False,
                    help='ouput file name')

parser.add_argument('-f', '--filter' , dest='filter', action='store', type=float, default=0.10, required=False,
                    help='filter FDR threshold (<) - default = 0.10')


parser.add_argument("-t",'--threshold', dest='threshold', action='store', type=int, default=1, required=False,
                    help='minimum read for interaction threshold (>=) - default = 1 (no filtering)')
parser.add_argument('-c', '--counts' ,action='store_true', dest='counts', help='store counts instead of FDR value')
parser.add_argument('-v', '--old_washu' ,action='store_true', dest='old', help='use old washu format instead of longrange')

args = parser.parse_args()

if args.outputfile:
    outputname=args.outputfile
else:
    outputname=args.inputfile + ".washu.txt"
FDR_thres = args.filter
Old_washu = args.old
counts = args.counts
ID_counter = 1

inputname=args.inputfile
if not os.path.isfile(inputname):
    raise Exception("input file couldn't be opened")

with open(outputname, "w") as outputfile, open( inputname, "r") as inputfile:
    for line in inputfile:
        data = line.split("\t")
        if float(data[7].strip()) > FDR_thres:
            # do nothing if FDR value is above FDR
            continue
        if args.threshold <= int(data[6]):
            # filter for threshold of read count
            if counts:
                score = data[6]
            else:
                score = str(1-float(data[7].strip()))
            if Old_washu:
                outputfile.write("{},{},{}\t{},{},{}\t{}\n".format(data[0],data[1],data[2],data[3],data[4],data[5],score))
            else:
                outputfile.write("{}\t{}\t{}\t{}:{}-{},{}\t{}\t{}\n".format(data[0],data[1],data[2],data[3],data[4],data[5],score,str(ID_counter),"."))
                ID_counter = ID_counter + 1
                outputfile.write("{}\t{}\t{}\t{}:{}-{},{}\t{}\t{}\n".format(data[3],data[4],data[5],data[0],data[1],data[2],score,str(ID_counter),"."))
                ID_counter = ID_counter + 1


if not Old_washu:
    import subprocess
    subprocess.run(["sort","-o",outputname,"-k1,1","-k2,2n",outputname])
    subprocess.run(["bgzip",outputname])
    subprocess.run(["tabix","-p","bed",outputname+".gz"])