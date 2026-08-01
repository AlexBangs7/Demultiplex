#!/usr/bin/env python

import argparse
import bioinfo
import gzip
from itertools import permutations

# Set up args
def get_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("-q", "--qscore", help="q-score cutoff for unknown indexes", required=False)
    return parser.parse_args()
args = get_args()


# Establish index and fastq files
directory = "/projects/bgmp/shared/2017_sequencing/"
index_file = directory + "indexes.txt"
R1_file = directory + "1294_S1_L008_R1_001.fastq.gz"
R2_file = directory + "1294_S1_L008_R2_001.fastq.gz"
R3_file = directory + "1294_S1_L008_R3_001.fastq.gz"
R4_file = directory + "1294_S1_L008_R4_001.fastq.gz"


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
            index_length = len(index1[4])

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

matched, hopped, indexes = index_pairing(index_file)

print(matched)
# Open output files for use later
# Matched outputs (48)
mfs = {}
for index in indexes:
    mfs[index] = (open(f'output/{index}_R1.fq', 'w'), open(f'output/{index}_R2.fq', 'w'))
mfs["GTAGCGTA"][0].write("hello")
# Hopped outputs (2)
hfs = {}
hfs["hopped"] = (open(f'output/hopped_R1.fq','w'), open(f'output/hopped_R2.fq','w'))
# Unknown outputs (2)
ufs = {}
ufs["unknown"] = (open(f'output/unknown_R1.fq','w'), open(f'output/unknown_R2.fq','w'))

# 3. Demultiplex function

def demultiplex(Read1:str,Read2:str,Read3:str,Read4:str, matched_indexes:dict, hopped_indexes:dict, qscore_cutoff:int):
    with gzip.open(Read1,"rt") as R1, gzip.open(Read2,"rt") as R2, gzip.open(Read3,"rt") as R3, gzip.open(Read4,"rt") as R4:
        line = 0
        r1_record = []
        r2_record = []
        r3_record = []
        r4_record = []            
        while True:
            r1_record.append(R1.readline().strip("\n"))
            r2_record.append(R2.readline().strip("\n"))
            r3_record.append(R3.readline().strip("\n"))
            r4_record.append(R4.readline().strip("\n"))
            r3_record[1] = bioinfo.reverse_comp(r3_record[1])

            if line % 4 == 3:
                r1_record[0] += f'{r2_record[1]}+{r3_record[1]}'
                r4_record[0] += f'{r2_record[1]}+{r3_record[1]}'
            
            R2score = bioinfo.qual_score(r2_record[3])
            R3score = bioinfo.qual_score(r3_record[3])

            if R2score or R3score <= qscore_cutoff: # unknown
                pass
            elif r2_record[1] or r3_record not in indexes: # unknown index or index with Ns
                pass
                #unknown_indexes += 1
            elif r2_record[1] != r3_record[1]: # hopped
                pass
                hopped_indexes[f'{r2_record[1]}+{r3_record[1]}'] += 1
            else: # matched
                pass
                matched_indexes[f'{r2_record[1]}+{r3_record[1]}'] += 1
            line +=1 


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