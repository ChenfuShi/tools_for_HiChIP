## Author: Chenfu Shi
## Last update date: 1/08/2018
## Contact: chenfu.shi@postgrad.manchster.ac.uk
## This software is distributed without any guarantee on it's functionality

# current HiCpro does not support paired end reads with qnames with a .1 and a .2 at the end based on the read
# the easiest way to solve this problem is to remove the .1 and .2
# this script takes the files from NCBI SRA format in input and then saves the  cleaned fastq.gz file


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