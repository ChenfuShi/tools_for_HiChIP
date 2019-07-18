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

# converts bedpe to long range, making sure to print twice each line.
# allows the user to choose which field to copy over and if you want to do -log10 for eg. p-values or q-values


import argparse
import subprocess
import math
import os

parser = argparse.ArgumentParser(description='Tool to convert bedpe files to long_range format. Uses bgzip and tabix to compress and index the file')




parser.add_argument("-i",'--input', dest='inputfile', action='store', required=True,
                    help='input file name')
parser.add_argument("-o",'--output', dest='outputfile', action='store', required=False,
                    help='ouput file name. Will add .gz automatically')
parser.add_argument("-f",'--field', dest='field', action='store', type=int, default=8, required=False,
                    help='field to store as score. Default 8th field. For MAPS use 9 for FDR')
parser.add_argument('-l', '--log' ,action='store_true', dest='log', help='do -log10 of score')


args = parser.parse_args()
args = parser.parse_args()

if args.outputfile:
    outputname=args.outputfile
else:
    outputname=args.inputfile + ".washu.bed"

inputname=args.inputfile
if not os.path.isfile(inputname):
    raise Exception("input file couldn't be opened")

ID_counter = 1


with open(outputname, "w") as outputfile, open(args.inputfile , "r") as inputfile:
    for line in inputfile:
        data = line.split("\t")
        chr1 = data[0].strip()
        if not data[1].strip().isdigit():
            # check that the line contains data instead of header
            continue
        start1 = data[1].strip()
        end1 = data[2].strip()
        chr2 = data[3].strip()
        start2 = data[4].strip()
        end2 = data[5].strip()
        score = data[args.field-1].strip()
        if args.log == True:
            try:
                score = str(-math.log10(float(score)))
            except ValueError:
                # in case the score is zero
                score = 384
        outputfile.write("{}\t{}\t{}\t{}:{}-{},{}\t{}\t{}\n".format(chr1,start1,end1,chr2,start2,end2,score,str(ID_counter),"."))
        ID_counter = ID_counter + 1
        outputfile.write("{}\t{}\t{}\t{}:{}-{},{}\t{}\t{}\n".format(chr2,start2,end2,chr1,start1,end1,score,str(ID_counter),"."))
        ID_counter = ID_counter + 1
        

# automatically sort, compress and index the output file
subprocess.run(["sort","-o",outputname,"-k1,1","-k2,2n",outputname])
subprocess.run(["bgzip",outputname])
subprocess.run(["tabix","-p","bed",outputname+".gz"])