#!/usr/bin/env python

import argparse
import bioinfo
import gzip
from itertools import permutations

# Set up args

def get_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("-q", "--qscore", help="q-score cutoff for unknown indexes", required=True)
    parser.add_argument("-t", "--test", help="if using test files", choices=[None, 'zipped', 'unzipped'], required=False)
    return parser.parse_args()
args = get_args()

args.qscore = int(args.qscore)

# Establish index and fastq files

if args.test == 'zipped': # Zipped test files
    directory = "/projects/bgmp/abangs/bioinfo/Bi622/Demultiplex/"
    index_file = directory + "Test_indexes.txt"
    R1_file = directory + "TEST-input_FASTQ/R1.fastq.gz"
    R2_file = directory + "TEST-input_FASTQ/R2.fastq.gz"
    R3_file = directory + "TEST-input_FASTQ/R3.fastq.gz"
    R4_file = directory + "TEST-input_FASTQ/R4.fastq.gz"
    output_folder = directory + "TEST-output_FASTQ/"


if args.test == 'unzipped': # Unzipped test files
    directory = "/projects/bgmp/abangs/bioinfo/Bi622/Demultiplex/"
    index_file = directory + "TEST-input_FASTQ/Test_indexes.txt"
    R1_file = directory + "TEST-input_FASTQ/R1.fastq"
    R2_file = directory + "TEST-input_FASTQ/R2.fastq"
    R3_file = directory + "TEST-input_FASTQ/R3.fastq"
    R4_file = directory + "TEST-input_FASTQ/R4.fastq"
    output_folder = directory + "TEST-output_FASTQ/"


else: # Files for actual demultiplexing sequence
    directory = "/projects/bgmp/shared/2017_sequencing/"
    index_file = directory + "indexes.txt"
    R1_file = directory + "1294_S1_L008_R1_001.fastq.gz"
    R2_file = directory + "1294_S1_L008_R2_001.fastq.gz"
    R3_file = directory + "1294_S1_L008_R3_001.fastq.gz"
    R4_file = directory + "1294_S1_L008_R4_001.fastq.gz"
    output_folder = "/projects/bgmp/abangs/bioinfo/Bi622/Demultiplex/Assignment-the-third/outputs/"

# Create dictionaries of matched and hopped index pairs

def index_pairing(index_file:str):
    ''' When provided a tab separated file containing indexes, output two dictionaries: one with all matched index pairs as keys and one with all hopped index pairs as keys (and zeroes as values for both)'''
    index_set = set() # empty
    with open(index_file, "r") as index_fh: 
        index_fh.readline() # Skip header

        # Check first index for correct sequence location, and add it if so
        index1 = index_fh.readline().strip().split()
        if bioinfo.validate_base_seq(index1[4]) == False:
            raise TypeError("Provided file does not have index sequences in expected column")
        else:
            index_set.add(index1[4])
            # index_length = len(index1[4])

        # Add each index to set
        for line in index_fh:
            line = line.strip().split()
            index_set.add(line[4])

    # Create dictionary for matched index pairs
    matched_indexes = {}
    for index in index_set:
        matched_indexes[f'{index}-{index}'] = 0

    # Create dictionary for hopped index pairs
    hopped_indexes = {}
    for hopped_pair in list(permutations(index_set, r=2)):
        hopped_indexes[f'{hopped_pair[0]}-{hopped_pair[1]}'] = 0

    return matched_indexes, hopped_indexes, index_set
# matched, hopped, indexes = index_pairing(index_file)


# Open output files for use later

def open_outputs(output_folder:str, indexes:set):
    mfs = {} # Matched outputs (48)
    hfs = {} # Hopped outputs (2)
    ufs = {} # Unknown outputs (2)
    if args.test: # Direct outputs to TEST-output_FASTQ folder
        for index in indexes:
            mfs[index] = (open(f'{output_folder}{index}_R1.fq', 'w'), open(f'{output_folder}{index}_R2.fq', 'w'))
        hfs["hopped"] = (open(f'{output_folder}hopped_R1.fq','w'), open(f'{output_folder}hopped_R2.fq','w'))
        ufs["unknown"] = (open(f'{output_folder}unknown_R1.fq','w'), open(f'{output_folder}unknown_R2.fq','w'))
    else: # Direct outputs to outputs folder
        for index in indexes:
            mfs[index] = (open(f'{output_folder}{index}_R1.fq', 'w'), open(f'{output_folder}{index}_R2.fq', 'w'))
        hfs["hopped"] = (open(f'{output_folder}hopped_R1.fq','w'), open(f'{output_folder}hopped_R2.fq','w'))
        ufs["unknown"] = (open(f'{output_folder}unknown_R1.fq','w'), open(f'{output_folder}unknown_R2.fq','w'))
    counts_file = open(f'{output_folder}counts.txt', 'w')
    return mfs, hfs, ufs, counts_file

# 2.5 read record function

def read_record(file):
    record = []
    for line in range(4):
        record.append(file.readline().strip("\n"))
    return record


# 3. Demultiplex function

def demultiplex(Read1:str,Read2:str,Read3:str,Read4:str, index_file:str, output_folder:str, qscore_cutoff:int):

    matched_indexes, hopped_indexes, index_set = index_pairing(index_file)

    mfs, hfs, ufs, counts = open_outputs(output_folder,index_set)

    if args.test == None or args.test == 'zipped':
        read = gzip.open
    else:
        read = open

    with read(Read1,"rt") as R1, read(Read2,"rt") as R2, read(Read3,"rt") as R3, read(Read4,"rt") as R4:
        unknown_indexes = 0
        while True:
            r1_record = read_record(R1)
            r2_record = read_record(R2)
            r3_record = read_record(R3)
            r4_record = read_record(R4)
            r3_record[1] = bioinfo.reverse_comp(r3_record[1])
            if r1_record[0] == "":
                break

            r1_record[0] += f' {r2_record[1]}-{r3_record[1]}'
            r4_record[0] += f' {r2_record[1]}-{r3_record[1]}'
            
            R2score = bioinfo.qual_score(r2_record[3])
            R3score = bioinfo.qual_score(r3_record[3])

            if R2score <= qscore_cutoff or R3score <= qscore_cutoff: # unknown
                for i in range(4):
                    ufs["unknown"][0].write(f'{r1_record[i]}\n')
                    ufs["unknown"][1].write(f'{r4_record[i]}\n')
                unknown_indexes += 1
            elif r2_record[1] not in index_set or r3_record[1] not in index_set: # unknown index or index with Ns
                for i in range(4):
                    ufs["unknown"][0].write(f'{r1_record[i]}\n')
                    ufs["unknown"][1].write(f'{r4_record[i]}\n')
                unknown_indexes += 1
            elif r2_record[1] != r3_record[1]: # hopped
                for i in range(4):
                    hfs["hopped"][0].write(f'{r1_record[i]}\n')
                    hfs["hopped"][1].write(f'{r4_record[i]}\n')
                hopped_indexes[f'{r2_record[1]}-{r3_record[1]}'] += 1
            else: # matched
                for i in range(4):
                    mfs[f'{r2_record[1]}'][0].write(f'{r1_record[i]}\n')
                    mfs[f'{r2_record[1]}'][1].write(f'{r4_record[i]}\n')
                matched_indexes[f'{r2_record[1]}-{r3_record[1]}'] += 1

    counts.write('Barcode\tCount\n')
    for k,v in matched_indexes.items():
        counts.write(f'{k}\t{v}\n')
    for k,v in hopped_indexes.items():
        counts.write(f'{k}\t{v}\n')
    counts.write(f'Unknowns\t{unknown_indexes}\n')

demultiplex(R1_file,R2_file,R3_file,R4_file,index_file,output_folder,args.qscore)