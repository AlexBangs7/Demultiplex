#!/usr/bin/env python

import argparse
import bioinfo
from itertools import permutations

# Set up args
def get_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("-q", "--qscore", help="q-score cutoff for unknown indexes", required=True)
    return parser.parse_args()
args = get_args()


# Establish index and fastq files
directory = "/projects/bgmp/shared/2017_sequencing/"
index_file = directory + "indexes.txt"
R1 = directory + "1294_S1_L008_R1_001.fastq.gz"
R2 = directory + "1294_S1_L008_R2_001.fastq.gz"
R3 = directory + "1294_S1_L008_R3_001.fastq.gz"
R4 = directory + "1294_S1_L008_R4_001.fastq.gz"


# Create dictionaries of matched and hopped index pairs
def index_pairing(index_file:str):
    ''' When provided a tab separated file containing indexes, output two dictionaries: one with all matched index pairs as keys and one with all hopped index pairs as keys (and zeroes as values for both)'''
    index_set = set() # empty
    with open(index_file, "r") as index_fh: 
        index_fh.readline()                                        # Skip header

        # Check first index for correct sequence location, and add it if so
        index1 = index_fh.readline().strip().split()
        if bioinfo.validate_base_seq(index1[4]) == False:
            raise TypeError("Provided file does not have index sequences in expected column")
        else:
            index_set.add(index1[4])

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

    return matched_indexes, hopped_indexes

print(len(index_pairing(index_file)[0]))


# 3. Demultiplex function

def demultiplex(R1:str,R2:str,R3:str,R4:str, matched_indexes, hopped_indexes, qscore_cutoff):
    
    pass
# define demultiplex(R1, R2, R3, R4, index_pairs, qscore_cutoff): 
#     ``` Provided four fastq files (two containing biological reads and two containing index reads), a dictionary containing all index pairs, and a qscore cutoff set by the user. Return two fastq files for each matching index-pair, two fastq files for all hopped index-pairs, two fastq files for all unknown index-pairs, and finally a tsv files with counts of all matched and hopped index-pairs ```

#     unknown_count = 0
#     WITH R1 open as R1, R2 open as R2, R3 open as R3, R4 open as R4: # Using gzip

#         WHILE True:
#             headers = read header for R1 and R4
#             skip headers for R2 and R3 # readline but don't assign to variable
#             R1seq, R4seq = read biological sequence from R1 and R4
#             R2seq, R3seq = read index sequence from R2 and R3
#             skip + in each file # readline but don't assign to variable
#             qscores = read qscores for each file
#             reverse_complement R3 sequence

#                 IF R2 quality score OR R3 quality score <= qscore cutoff:
#                     open Unknown FASTQ files
#                     append R1 record to Unknown_R1 file with indexes added to end of header (index1-reverse complement index2)
#                     append R4 record Unknown_R4 file with indexes added to end of header (index1-reverse complement index2)
#                     +1 unknown_count

#                 ELIF "R2_index-R3_index" not in index_pairs dictionary:
#                     open Unknown FASTQ files
#                     append R1 record to Unknown_R1 file with indexes added to end of header
#                     append R4 record to Unknown_R4 file with indexes added to end of header
#                     +1 unknown_count

#                 ELIF Index1_read == reverse complement of Index2_read:
#                     open Index1-Index2 FASTQ files
#                     append R1 record to [Index]_R1 output file with indexes added to end of header
#                     append record information of R4 to [Index]_R4 output file with indexes added to end of header

#                 ELSE (IF Index1_read != reverse complement of Index2_read):
#                     open Index-hopped FASTQ files
#                     append R1 record to Hopped_R1 file with indexes added to end of header
#                     append R4 record to Hopped_R4 file with indexes added to end of header

#             break if R1_header is equivalent to an empty string
#         Write filled index_pairs dictionary and unknown count to a index_pairs tsv
#          file
#         Return matched, hopped, and unknown files
#         Return index_pairs tsv file

# Input: TEST-input-FASTQ files
# Expected output: TEST-output-FASTQ files
# ```