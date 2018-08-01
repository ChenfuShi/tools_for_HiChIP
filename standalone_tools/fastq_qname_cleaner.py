#HiCpro does not support paired end reads with qnames with a .1 and a .2 at the end based on the read
#the easiest way to solve this problem is to remove the .1 and .2
#this script takes the file in input and then saves the  cleaned fastq.gz file

import os
import argparse
import gzip

parser = argparse.ArgumentParser(description='remove .1 or .2 from qnames in fastq.gz file.')

parser.add_argument("-i",'--input', dest='inputfile', action='store', required=True,
                    help='input file name (gzipped fastq)')
parser.add_argument("-o",'--output', dest='outputfile', action='store', required=True,
                    help='ouput file name (gzipped fastq)')

args = parser.parse_args()

if os.path.exists('args.inputfile') == False:
    raise Exception('Couldn\'t find input file')
if os.path.exists('args.outputfile') == True:
    raise Exception('Output file is present, will NOT attempt to overwrite')

with gzip.open(args.outputfile, "wb") as outputfile, gzip.open(args.inputfile , "rb") as inputfile:
    for read in inputfile:
        if read[0] == "+" or read[0] == "@":
            print(read)
            a=read.split(" ")
            a[0] = a[0][:-2]
            read = " ".join(a)
        outputfile.write(read)