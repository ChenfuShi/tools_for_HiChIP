#HiCpro does not support paired end reads with qnames with a .1 and a .2 at the end based on the read
#the easiest way to solve this problem is to remove the .1 and .2
#this script takes the file in input and then saves the  cleaned fastq.gz file

import os
import argparse


parser = argparse.ArgumentParser(description='remove .1 or .2 from fastq.gz file.')

parser.add_argument("-i",'--input', dest='inputfile', action='store', required=True,
                    help='input file name')
parser.add_argument("-o",'--output', dest='outputfile', action='store', required=True,
                    help='ouput file name')

args = parser.parse_args()
print(args.inputfile)