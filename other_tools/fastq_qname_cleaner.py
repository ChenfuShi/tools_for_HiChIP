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

# current HiCpro does not support paired end reads with qnames with a .1 and a .2 at the end based on the read
# this can be a problem if you downloaded files from SRA with the -I setting.
# the easiest way to solve this problem is to remove the .1 and .2 or download again the files.
# this script takes the files from NCBI SRA format in input and then saves the cleaned fastq.gz file


import argparse
import gzip

parser = argparse.ArgumentParser(description='remove .1 or .2 from qnames in fastq.gz file.')

parser.add_argument("-i",'--input', dest='inputfile', action='store', required=True,
                    help='input file name (gzipped fastq)')
parser.add_argument("-o",'--output', dest='outputfile', action='store', required=True,
                    help='ouput file name (gzipped fastq)')

args = parser.parse_args()

with gzip.open(args.outputfile, "wt", compresslevel=5) as outputfile, gzip.open(args.inputfile , "rt") as inputfile:
    for read in inputfile:
        if read[0:2] == "+S" or read[0:2] == "@S":
            a=read.split(" ")
            a[0] = a[0][:-2]
            read = " ".join(a)
        outputfile.write(read)