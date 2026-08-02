#!/usr/bin/env python

import bioinfo
import gzip
import argparse
import matplotlib.pyplot as plt

def get_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("-r", "--read", help="read number", required=True)
    parser.add_argument("-f", "--file", help="File location", required=False)
    parser.add_argument("-t", "--test", help="Is this a test run?", required=False)
    return parser.parse_args()
args = get_args()

read = args.read

if args.file:
    input_file = args.file
elif args.test:
    input_file = f"./TEST-input_FASTQ/{read}.fastq"
else:
    #print("Not Test")
    input_file = f"/projects/bgmp/shared/2017_sequencing/1294_S1_L008_{read}_001.fastq.gz"

zp = True if input_file[-3:] == ".gz" else False
# fh = gzip.open(input_file,"rt") if zp else open(input_file,"r")

def init_list(lst: list, file: str = input_file, value: float=0.0):
    '''This function takes an empty list and a fastq  and will populate the list with
    "value". The list will be as long as the first sequence in the fastq file.'''
    fh = gzip.open(file,"rt") if zp else open(file,"r")
    fh.readline()
    num_bases = len(fh.readline().strip('\n'))
    fh.close()
    lst = [value] * num_bases
    return lst, num_bases

def populate_list(file: str = input_file) -> tuple[list, int]:
    """Provided a fastq file, run init list and populate 
    list with the sum of each base positions' phred scores"""
    score_list= []
    score_list, num_bases = init_list(score_list, file)
    if zp:
        fh = gzip.open(file,"rt")
    else:
        fh = open(file,"r")
    i = 0
    for line in fh:
        i+=1
        line = line.strip('\n')
        if i%4 == 0:
            for base in range(num_bases):
                score = bioinfo.convert_phred(line[base])
                score_list[base] += score
    for base in range(num_bases):
        score_list[base] = score_list[base]/(i/4)
    fh.close()
    return score_list, i

mean_scores, num_lines = populate_list(input_file)

if read != None: # If a read number is provided, print to file named RX_distribution.tsv
    with open(f"Assignment-the-first/outputs/{read}_distribution.tsv","w") as tsv:
        tsv.write("# Base Pair\tMean Quality Score\n")
        for position, score in enumerate(mean_scores):
            score = score
            tsv.write(f"{position}\t{score}\n")
else:
    print("No read provided")

pos=range(len(mean_scores))
scores=mean_scores
plt.bar(pos,scores)
plt.ylim(0,44)
plt.ylabel("Quality Score")
plt.xlabel("Base Position")
plt.title(f"Quality Score Distribution of {read}")
plt.savefig(f'Assignment-the-first/outputs/{read}_distribution.png')