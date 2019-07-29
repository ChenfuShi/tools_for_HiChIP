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


# converts longrange format to bedpe
# because longrange should be two lines per interaction create a set and check that it wasn't already printed.


import argparse
import subprocess
import gzip
import os
parser = argparse.ArgumentParser(description='Tool to convert long_range format to bedpe')



parser.add_argument("-i",'--input', dest='inputfile', action='store', required=True,
                    help='input file name')
parser.add_argument("-o",'--output', dest='outputfile', action='store', required=False,
                    help='ouput file name')

args = parser.parse_args()

if args.outputfile:
    outputname=args.outputfile
else:
    outputname=args.inputfile + ".bedpe"

inputname=args.inputfile
if not os.path.isfile(inputname):
    raise Exception("input file couldn't be opened")

with gzip.open(inputname, "rt") as input_file, open(outputname,"w") as output_file:
    interactions_set = set()
    for line in input_file:
        # get line properties
        chrA = line.split("\t")[0].strip()
        startA = int(line.split("\t")[1].strip())
        endA = int(line.split("\t")[2].strip())
        B = line.split("\t")[3].strip().split(":")
        chrB = B[0].strip()
        startB = int(B[1].strip().split("-")[0].strip())
        endB = int(B[1].strip().split("-")[1].split(",")[0].strip())
        score = B[1].strip().split(",")[1].strip()
        ID = line.split("\t")[4].strip()
        # generate the two possible lines, then check if present in set, if not present in either version print out one with ID
        outA = f"{chrA}{startA}{endA}{chrB}{startB}{endB}{score}"
        outB = f"{chrB}{startB}{endB}{chrA}{startA}{endA}{score}"
        if outA in interactions_set or outB in interactions_set:
            continue
        else:
            interactions_set.add(outA)
            interactions_set.add(outB)
            output_file.write(f"{chrA}\t{startA}\t{endA}\t{chrB}\t{startB}\t{endB}\t{ID}\t{score}\n")



