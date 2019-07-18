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

#This tool extracts regions of interest from hichipper data
# only interactions starting of ending within those regions will be outputed
# the anchors just need to touch the region to work(could theoretically just have a 1bp region)
# with the new format you need two lines for loci. but expect the input file to be already formatted correctly with two lines. 
# also with new format expects the file to be gzipped

import argparse
import subprocess
import os
import gzip
parser = argparse.ArgumentParser(description='Tool to extract a specific region of interest (anchor) from hichipper or CHiCAGO washu data. Uses bgzip and tabix to compress and index the file')




parser.add_argument("-i",'--input', dest='inputfile', action='store', required=True,
                    help='input file name')
parser.add_argument("-o",'--output', dest='outputfile', action='store', required=False,
                    help='ouput file name. Will add .gz automatically')
parser.add_argument("-c",'--chrom', dest='chrom', action='store', required=True,type = str,
                    help='chromosome')
parser.add_argument("-s",'--start', dest='region_start', action='store', required=True,type = int,
                    help='start of region of interest')
parser.add_argument("-e",'--end', dest='region_end', action='store', required=True,type = int,
                    help='start of region of interest')
parser.add_argument('-v', '--old_washu' ,action='store_true', dest='old', help='use old washu format instead of longrange')



args = parser.parse_args()

Old_washu = args.old
if args.outputfile:
    outputname=args.outputfile
else:
    outputname=args.inputfile + ".extract_region.txt"

chrom = args.chrom
region_start = args.region_start
region_end = args.region_end

inputname=args.inputfile
if not os.path.isfile(inputname):
    raise Exception("input file couldn't be opened")



if Old_washu:
    #old format washu processing
    with open(inputname, "r") as input_file, open(outputname,"w") as output_file:
        for line in input_file:
            # split the line by the tab. old format is loc1 loc2 score. next line gets a list with the two locs, then split again for coords.
            location = line.split()[0:2]
            for val in location:
                if val.split(",")[0] == chrom and ((int(val.split(",")[1]) <= region_end and int(val.split(",")[1]) >= region_start) or (int(val.split(",")[2]) <= region_end and int(val.split(",")[2]) >= region_start) or (int(val.split(",")[2]) >= region_end and int(val.split(",")[1]) <= region_start)): 
                    output_file.write(line)
                    # break just doesn't allow a line to be written twice
                    break

else:
    #new format washu processing
    with gzip.open(inputname, "rt") as input_file, open(outputname,"w") as output_file:
        for line in input_file:
            # new format has loc1 and 2 that are different format. next few lines format everything correctly and uses a if similar to the one for old format.
            chrA = line.split()[0]
            startA = int(line.split()[1])
            endA = int(line.split()[2])
            B = line.split()[3].split(":")
            chrB = B[0]
            startB = int(B[1].split("-")[0])
            endB = int(B[1].split("-")[1].split(",")[0])

            location = [(chrA,startA,endA),(chrB,startB,endB)]

            for val in location:
                if val[0] == chrom and ((val[1] <= region_end and val[1] >= region_start) or (val[2] <= region_end and val[2] >= region_start) or (val[2] >= region_end and val[1] <= region_start)): 
                    output_file.write(line)
                    # break just doesn't allow a line to be written twice
                    break   
    # processes the file, sort, compress and index the output file
    subprocess.run(["sort","-o",outputname,"-k1,1","-k2,2n",outputname])
    subprocess.run(["bgzip",outputname])
    subprocess.run(["tabix","-p","bed",outputname+".gz"])



        
