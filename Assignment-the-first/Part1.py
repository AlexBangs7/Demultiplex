#!/usr/bin/env python
import bioinfo
import gzip
import argparse
from matplotlib import pyplot as plt


def get_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="file_name", required=True)
    parser.add_argument("-r", "--read", help="read number", required=False)
    return parser.parse_args()
args = get_args()
input_file = args.file
read = args.read

zp = True if input_file[-3:] == ".gz" else False
fh = gzip.open(input_file,"rt") if zp else open(input_file,"r")


def init_list(lst: list, file: str = input_file, value: float=0.0) -> list:
    '''This function takes an empty list and a fastq  and will populate the list with
    "value". The list will be as long as the first sequence in the fastq file.'''
    fh = gzip.open(file,"rt") if zp else open(file,"r")
    fh.readline()
    bases = len(fh.readline().strip('\n'))
    fh.close()
    lst = [value] * bases
    return lst

def populate_list(file: str = input_file) -> tuple[list, int]:
    """Update with your own docstring"""
    my_list: list = []
    my_list = init_list(my_list, file)
    if zp:
        fh = gzip.open(file,"rt")
    else:
        fh = open(file,"r")
    i = 0
    for line in fh:
        i+=1
        line = line.strip('\n')
        if i%4 == 0:
            for I in range(len(line)):
                score = bioinfo.convert_phred(line[I])
                my_list[I] += score
    fh.close()
    return my_list, i

my_list, num_lines = populate_list(input_file)


if read != None: # If a read number is provided, print to file named RX_distribution.tsv
    with open(f"{read}_distribution.tsv","w") as tsv:
        tsv.write("# Base Pair\tMean Quality Score")
        for position, score in enumerate(my_list):
            score = score/(num_lines/4)
            tsv.write(f"{position}\t{score}\n")
else:
    print("No read provided")




from matplotlib import pyplot as plt

x=range(101)
y=my_list
plt.hist(x,y)
plt.ylim(0,44)
plt.savefig(f'{read}_distribution.png')