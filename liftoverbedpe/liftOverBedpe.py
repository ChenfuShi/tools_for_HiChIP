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


#### This software is adapted from https://github.com/dphansti/liftOverBedpe
# Things have been changed because it wasn't working and this one supports more columns

#########################################

# This software requires Liftover to be present in the environment

# for our server: 
# module load apps/binapps/liftover  
# --lift liftover --chain  NO PATH
# hg18ToHg19.over.chain.gz  hg19ToHg18.over.chain.gz  hg38ToHg19.over.chain.gz  mm9ToMm10.over.chain.gz
# hg18ToHg38.over.chain.gz  hg19ToHg38.over.chain.gz  mm10ToMm9.over.chain.gz


import argparse
import os
import pandas as pd


def splitBedpe(bedpe,tmp1="tmp1.bed",tmp2="tmp2.bed",header=False,verbose=False):
	""" Function that splits up bedpe files into 2 temp files """
	if header:
		inputBedpe = pd.read_csv(bedpe,sep="\t")
	else:
		inputBedpe = pd.read_csv(bedpe,sep="\t",header=None)
	num_cols = len(inputBedpe.columns)
	id_col = num_cols
	inputBedpe[id_col] = inputBedpe.index
	inputBedpe.iloc[:,[0,1,2,id_col]].to_csv("tmp1.bed", sep="\t", header = False, index = False)
	inputBedpe.iloc[:,[3,4,5,id_col]].to_csv("tmp2.bed", sep="\t", header = False, index = False)
	if num_cols > 6:
		extra_data = inputBedpe.iloc[:,list(range(6,num_cols))].copy()
		return extra_data
	else:
		return None


def doliftOver(liftOver,chain,infile,verbose=False):
	""" Function that implements liftOver """
	cmd = " ".join([liftOver,infile,chain,infile + ".success",infile + ".failure"])
	if verbose:
		print(cmd)
	os.system(cmd)
	

def mergeliftOver(f1,f2,extra_data,outputfile,verbose=False):
	""" Function that merges liftOver """
	sideA = pd.read_csv(f1, header = None, sep="\t", index_col = 3)
	sideB = pd.read_csv(f2, header = None, sep="\t", index_col = 3)
	merged = sideA.merge(sideB,left_index=True,right_index=True,validate ="one_to_one")
	if extra_data is not None:
		merged = merged.merge(extra_data,left_index=True,right_index=True,validate ="one_to_one")
	merged.to_csv(outputfile, sep="\t", header = False, index = False)



if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='wrapper for liftOver to accomodate bedpe files')

	parser.add_argument("-i",'--input', dest='infile', action='store', required=True,
                    help='input file name')
	parser.add_argument("-o",'--output', dest='outfile', action='store', required=True,
						help='ouput file name')
	parser.add_argument("-v",'--verbose', dest='verbose', action='store_true', default=False, required=False,
						help='Verbose')
	parser.add_argument("-t",'--header', dest='header', action='store_true', default=False, required=False,
						help='If file has a 1-line header')
	parser.add_argument("-l",'--lift', dest='liftOver', action='store', required=True,
                    help='path to liftOver')
	parser.add_argument("-c",'--chain', dest='chain', action='store', required=True,
						help='path to chain file')

	# parse arguments
	args = parser.parse_args()

	# read in args
	LO       = args.liftOver
	chain    = args.chain
	bedpeIN  = args.infile
	bedpeOUT = args.outfile
	tmp1     = "tmp1.bed"
	tmp2     = "tmp2.bed"
	header	 = args.header
	verbose	 = args.verbose

	# break up the files
	extra_data = splitBedpe(bedpeIN,tmp1,tmp2,header,verbose)

	# perform liftOver
	doliftOver(LO,chain,tmp1,verbose)
	doliftOver(LO,chain,tmp2,verbose)

	# merge liftOvered files
	mergeliftOver(tmp1+".success",tmp2+".success",extra_data,bedpeOUT,verbose)

	# remove tmp files
	os.remove(tmp1)
	os.remove(tmp2)
	os.remove(tmp1+".success")
	os.remove(tmp1+".failure")
	os.remove(tmp2+".success")
	os.remove(tmp2+".failure")





















