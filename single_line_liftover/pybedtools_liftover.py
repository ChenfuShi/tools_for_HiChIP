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

# This software requires Liftover to be present in the environment
# Helper tool that you can import in python to liftover a pybedtools bed or a df.

# import sys
# sys.path.insert(0,"/mnt/iusers01/jw01/mdefscs4/communal_software/tools_for_HiChIP/single_line_liftover")
# import pybedtools_liftover


# for our server: 
# module load apps/binapps/liftover  
# --lift liftover --chain  NO PATH
# hg18ToHg19.over.chain.gz  hg19ToHg18.over.chain.gz  hg38ToHg19.over.chain.gz  mm9ToMm10.over.chain.gz
# hg18ToHg38.over.chain.gz  hg19ToHg38.over.chain.gz  mm10ToMm9.over.chain.gz
# this software takes a pybedtool format
# there's another chain file in NEW_references

import os
import pandas as pd
import subprocess
import pybedtools as pbed

SCRATCH = "/mnt/iusers01/jw01/mdefscs4/scratch/liftover_temp"

def get_liftover_pybedtools(bed_file, chain = "hg19ToHg38.over.chain.gz", 
                    LO = "/mnt/jw01-aruk-home01/projects/shared_resources/bin/liftover/liftover", 
                    tmp1 = "/mnt/iusers01/jw01/mdefscs4/scratch/liftover_temp/input_file.bed", 
                    verbose = False):

    os.makedirs(SCRATCH, exist_ok = True)
    cmd = " ".join([LO, bed_file.fn, chain, tmp1 + ".success", tmp1 + ".failure"])
    sts = subprocess.call("module load apps/binapps/liftover;" + cmd, shell=True, ) 

    return pbed.BedTool(tmp1+".success")


def get_liftover_df(df_in, columns = [0,1,2],
                    chain = "hg19ToHg38.over.chain.gz", 
                    LO = "/mnt/jw01-aruk-home01/projects/shared_resources/bin/liftover/liftover", 
                    tmp1 = "/mnt/iusers01/jw01/mdefscs4/scratch/liftover_temp/input_file.bed", 
                    verbose = False):
    df = df_in.copy()
    df['unique_id'] = df.index
    df_slice = df[columns + ['unique_id']].copy()
    
    bed_file = pbed.BedTool.from_dataframe(df_slice)

    os.makedirs(SCRATCH, exist_ok = True)
    cmd = " ".join([LO, bed_file.fn, chain, tmp1 + ".success", tmp1 + ".failure"])
    sts = subprocess.call("module load apps/binapps/liftover;" + cmd, shell=True, ) 

    df_mapped = pbed.BedTool(tmp1+".success").to_dataframe(header=None,disable_auto_names=True, names = "chr_lift start_lift end_lift unique_id".split())
    df = df.merge(df_mapped, left_on = "unique_id", right_on = "unique_id")
    df = df.drop("unique_id", axis = 1)
    return df