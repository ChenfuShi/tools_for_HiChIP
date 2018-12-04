#quick script to generate the annotation file for hichipper using the output from hicpro annotation

#basically is stripping the bed file from the resfrag file from hicpro

#chr1    0       11159   HIC_chr1_1      0       +
#gets converted to 
#chr1    0       11160

# note the number gets increased by one. that happens only on the end number because whatever
#moreover filter all the contigs and stuff and keep only 1-22+xy

inputfile = open("F:\\psa_functional_genomics\\HiChIP_test\\software\\HiCpro\\HiC-Pro_2.11.0-beta\\annotation\\hg38_arima.bed","r")

outputfile= open("arima_hg38.bed","w")

sanechr=["chr1","chr2","chr3","chr4","chr5","chr6","chr7","chr8","chr9","chr10","chr11","chr12","chr13","chr14","chr15","chr16","chr17","chr18","chr19","chr20","chr21","chr22","chrX","chrY"]

for line in inputfile:
    parts=line.split("\t")
    if parts[0] in sanechr:
        outputfile.write("{}\t{}\t{}\n".format(parts[0],parts[1],(int(parts[2])+1)))
