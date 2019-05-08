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

# converts the old washu interactions format(legacy) to the new one
# this software requires bgzip and tabix to be callable from environment



import argparse
import subprocess

parser = argparse.ArgumentParser(description='Tool to convert the legacy washu interactions to the new long_range format. Uses bgzip and tabix to compress and index the file')




parser.add_argument("-i",'--input', dest='inputfile', action='store', required=True,
                    help='input file name')
parser.add_argument("-o",'--output', dest='outputfile', action='store', required=False,
                    help='ouput file name. Will add .gz automatically')


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