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
import subprocess

SCRATCH = "/mnt/iusers01/jw01/mdefscs4/scratch/liftover_temp"

def _format_input(input_str):
    if not input_str.startswith("chr"):
        input_str = "chr" + input_str
    if ":" in  input_str:
        input_str = input_str.replace(":", "\t")
    if "-" in input_str:
        input_str = input_str.replace("-", "\t")
    if " " in input_str:
        input_str = input_str.replace(" ", "\t")
    return input_str

def single_liftover(input_str, LO = "/mnt/jw01-aruk-home01/projects/shared_resources/bin/liftover/liftover", chain = "hg19ToHg38.over.chain.gz", tmp1 = "/mnt/iusers01/jw01/mdefscs4/scratch/liftover_temp/input_file.bed", verbose = False):
    os.makedirs(SCRATCH, exist_ok = True)
    formated_string = _format_input(input_str)
    with open(tmp1, "w" ) as f:
        f.write(formated_string)
    cmd = " ".join([LO, tmp1,chain, tmp1 + ".success", tmp1 + ".failure"])
    sts = subprocess.call("module load apps/binapps/liftover;" + cmd, shell=True, )   
    if os.stat(tmp1 + ".failure").st_size == 0:
        with open(tmp1 + ".success") as f:
            successes = f.readlines()
            os.remove(tmp1)
            os.remove(tmp1+".success")
            os.remove(tmp1+".failure")
            if verbose:
                print(successes[0])
            return successes[0]
    else:
        with open(tmp1 + ".failure") as f:
            errors = f.readlines()
            if verbose:
                print(errors)
            os.remove(tmp1)
            os.remove(tmp1+".success")
            os.remove(tmp1+".failure")
            return errors


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='wrapper for liftOver for a single line')

    parser.add_argument("-i",'--input', dest='in_str', action='store', required=True,
                    help='input string')
    parser.add_argument("-l",'--lift', dest='liftOver', action='store', required=False, default = "/mnt/jw01-aruk-home01/projects/shared_resources/bin/liftover/liftover",
                    help='path to liftOver')
    parser.add_argument("-c",'--chain', dest='chain', action='store', required=False, default = "hg19ToHg38.over.chain.gz",
                        help='path to chain file, default is hg19 to hg38')
    parser.add_argument("-v",'--verbose', dest='verbose', action='store_true', default=False, required=False,
						help='Verbose')
    # parse arguments
    args = parser.parse_args()

    # read in args  
    LO       = args.liftOver
    chain    = args.chain
    IN  = args.in_str
    tmp1 = "input_file.bed"
    tmp1 = os.path.join(SCRATCH, tmp1)
    verbose	 = args.verbose

    # perform liftOver
    single_liftover(IN,LO,chain,tmp1,verbose)


