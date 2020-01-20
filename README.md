# Tools for HiChIP and Capture HiC analysis

This is a toolset developed for use as part of pipelines in the analysis of HiChIP and Capture HiC data in our lab at The University of Manchester.

### Table of Contents 
- [Tools for HiChIP and Capture HiC analysis](#tools-for-hichip-and-capture-hic-analysis)
    - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Tools](#tools)
    - [Washu legacy pairwise interaction to longrange converter](#washu-legacy-pairwise-interaction-to-longrange-converter)
    - [Viewpoint extract from pairwise interaction and longrange files](#viewpoint-extract-from-pairwise-interaction-and-longrange-files)
    - [Hichipper FDR and readcount filtering tool](#hichipper-fdr-and-readcount-filtering-tool)
    - [Converters to and from BEDPE to and from washu longrange](#converters-to-and-from-bedpe-to-and-from-washu-longrange)
    - [Liftover for Bedpe files](#liftover-for-bedpe-files)
    - [Other tools](#other-tools)
  - [Authors](#authors)
  - [License](#license)

## Installation

Currently all tools are written in plain python 3 for linux, so just download the repository and make sure that the requirements are satisfied and callable from command line.

Requirements:

* bgzip
* tabix

To download the repository
```
git clone https://github.com/ChenfuShi/tools_for_HiChIP.git
```

To update the repository
```
git pull origin master
```

## Tools

### Washu legacy pairwise interaction to longrange converter

This tool can be used to convert the pairwise interaction format that is used by the legacy  washu epigenome browser to the new long-range interaction format for the new washu browser.
It takes the txt file and converts it to the bed like format. It is then sorted, compressed and indexed. To use these files they need to be uploaded to a hosted webserver and then give the link to washu.

```
python washu_converter.py --help
usage: washu_converter.py [-h] -i INPUTFILE [-o OUTPUTFILE]

Tool to convert the legacy washu interactions to the new long_range format.
Uses bgzip and tabix to compress and index the file

optional arguments:
  -h, --help            show this help message and exit
  -i INPUTFILE, --input INPUTFILE
                        input file name
  -o OUTPUTFILE, --output OUTPUTFILE
                        ouput file name. Will add .gz automatically
```

### Viewpoint extract from pairwise interaction and longrange files

This tool can be used to extract viewpoints from the hichipper and CHiCAGO outputs for the washu epigenome browser. It supports both the new format and the legacy format.
To use just supply the genomic coordinates of the required viewpoint and it will output a file containing all the interactions that touch those coordinates.
For hichipper we suggest using the following tool first to filter the results by readcount and FDR.

```
python region_extract.py --help
usage: region_extract.py [-h] -i INPUTFILE [-o OUTPUTFILE] -c CHROM -s
                         REGION_START -e REGION_END [-v]

Tool to extract a specific region of interest (anchor) from hichipper washu
data. Uses bgzip and tabix to compress and index the file

optional arguments:
  -h, --help            show this help message and exit
  -i INPUTFILE, --input INPUTFILE
                        input file name
  -o OUTPUTFILE, --output OUTPUTFILE
                        ouput file name. Will add .gz automatically
  -c CHROM, --chrom CHROM
                        chromosome
  -s REGION_START, --start REGION_START
                        start of region of interest
  -e REGION_END, --end REGION_END
                        start of region of interest
  -v, --old_washu       use old washu format instead of longrange
```

### Hichipper FDR and readcount filtering tool

This tool can be used to filter the results from hichipper by FDR or number of reads supporting the interactions. It takes the interactions.all.mango file and outputs in washu ready format. Can output both the new format and the legacy format. If wanted can output the number of reads as the score instead of FDR values.
```
python hichipper2washuFDR.py --help
usage: hichipper2washuFDR.py [-h] -i INPUTFILE [-o OUTPUTFILE] [-f FILTER]
                             [-t THRESHOLD] [-v]

Convert hichipper mango output to washu pairwise interaction files and filters
with FDR scores and minimum number of reads. Uses bgzip and tabix to
compress and index the file

optional arguments:
  -h, --help            show this help message and exit
  -i INPUTFILE, --input INPUTFILE
                        input file name (interactions.all.mango file)
  -o OUTPUTFILE, --output OUTPUTFILE
                        ouput file name
  -f FILTER, --filter FILTER
                        filter FDR threshold (<) - default = 0.10
  -t THRESHOLD, --threshold THRESHOLD
                        minimum read for interaction threshold (>=) - default =
                        1 (no filtering)
  -c COUNTS, --counts COUNTS
                        store counts instead of FDR value             
  -v, --old_washu       use old washu format instead of longrange
```

### Converters to and from BEDPE to and from washu longrange
These two tools can be used to convert results from longrange to bedpe and revese.
From bedpe to longrange you can choose which column to copy over and if you want you can do -log10 for p-values etc.

```
python longrange2bedpe.py --help
usage: longrange2bedpe.py [-h] -i INPUTFILE [-o OUTPUTFILE]

Tool to convert long_range format to bedpe

optional arguments:
  -h, --help            show this help message and exit
  -i INPUTFILE, --input INPUTFILE
                        input file name
  -o OUTPUTFILE, --output OUTPUTFILE
                        ouput file name
```

```
python bedpe2longrange.py --help
usage: bedpe2longrange.py [-h] -i INPUTFILE [-o OUTPUTFILE] [-f FIELD] [-l]

Tool to convert bedpe files to long_range format. Uses bgzip and tabix to
compress and index the file

optional arguments:
  -h, --help            show this help message and exit
  -i INPUTFILE, --input INPUTFILE
                        input file name
  -o OUTPUTFILE, --output OUTPUTFILE
                        ouput file name. Will add .gz automatically
  -f FIELD, --field FIELD
                        field to store as score. Default 8th field. For MAPS
                        use 9 for FDR
  -l, --log             do -log10 of score
```

### Liftover for Bedpe files
This tool can be used to liftover bedpe files.
This is a wrapper for liftOver tool, it requires liftover in the system.

```
python liftOverBedpe.py --help
usage: liftOverBedpe.py [-h] -i INFILE -o OUTFILE [-v] [-t] -l LIFTOVER -c
                        CHAIN

wrapper for liftOver to accomodate bedpe files

optional arguments:
  -h, --help            show this help message and exit
  -i INFILE, --input INFILE
                        input file name
  -o OUTFILE, --output OUTFILE
                        ouput file name
  -v, --verbose         Verbose
  -t, --header          If file has a 1-line header
  -l LIFTOVER, --lift LIFTOVER
                        path to liftOver
  -c CHAIN, --chain CHAIN
                        path to chain file

```



### Other tools

These tools are not maintained but might be useful for someone

fastq name cleaner
```
Current HiCpro version does not support paired end reads with qnames with a .1 and a .2 at the end based on the read.
This can be a problem if you downloaded files from SRA with the -I setting.
The easiest way to solve this problem is to remove the .1 and .2 or download again the files.
This script takes the files from NCBI SRA format in input and then saves the cleaned fastq.gz file.
```

hichipper restriction file gen
```
Quick script to generate the annotation file for hichipper using the hicpro resfrag annotation bed
```


## Authors

These tools were developed by Chenfu Shi<sup>1</sup> at the University of Manchester for use in our pipelines in Magnus Rattray<sup>2,3</sup> and Gisela Orozco<sup>1,3</sup> labs.
1) Centre for Genetics and Genomics Versus Arthritis. Division of Musculoskeletal and Dermatological Sciences, School of Biological Sciences, Faculty of Biology, Medicine and Health, The University of Manchester, UK.
2) Division of Informatics, Imaging and Data Sciences, Faculty of Biology, Medicine and Health, University of Manchester, UK.
3) NIHR Manchester Biomedical Research Centre, Manchester University NHS Foundation Trust, Manchester Academic Health Science Centre, Manchester, UK.


This work was funded by the Wellcome Trust (award references 207491/Z/17/Z and 215207/Z/19/Z), Versus Arthritis (award reference 21754), NIHR Manchester BRC and the Medical Research Council (award reference MR/N00017X/1).


## License

The tools are released with a BSD-3-Clause License

```
BSD-3-Clause License
Copyright 2019 Chenfu Shi
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```
