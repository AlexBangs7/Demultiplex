## Problem:
Sort fastq reads based on indexes, ensuring that matching index-pairs are sorted together and that nonmatching and unknown index-pairs are sorted separately. In addition, count the index-hopped and unknown index-pairs to analyze sequencing efficiency.

## Output:
Files containing all reads that have the same index-pairs, two files for each matching pair.
Files containing all mismatched index-pairs
Files containing all unknown index-pairs.
Counts for the index-hopped and unknown index-pairs to analyze multiplexing efficiency.

## Psuedocode:
```
0. Set a qscore_cutoff

qscore_cutoff = X


1. Reverse complement function

define reverse_complement:
    ``` When provided a string of DNA/RNA, outputs the reverse complement ```

    loop thorugh sequence and make "reverse complement" string
    return "reverse complement" string

Input: GATTACA
Expected output: TGTAATC

2. Establish indexes and make index-pair dictionary

def index_sorting:
    ``` When provided a file with indexes in it, output a dictionary will all possible index-pairs as keys (and zeroes as values) ```

    index_set = {} # empty
    WITH index_file (tsv) open as file:  
        FOR row in file:
            Separate indexes
            Put index into index_set
    Convert index_set into index_list
    index_pairs = {} # empty dictionary
    FOR index1 in index_list:
        FOR index2 in index_list:
            convert index 2 to its reverse complement using reverse_complement function
            add f-string key of "index1-index2" to dictionary with starting value = 0
    return index_pairs dictionary containing all possible matched and hopped index-pairs

Input: file containing:
GACT    AAGT 
TCCA    AAGT

Expected Output:
index_pairs = {"GACT-CTGA": 0, "GACT-TTCA": 0, "GACT-AGGT": 0, "AAGT-CTGA": 0, "AAGT-TTCA": 0, 
"AAGT-AGGT": 0, "TCCA-CTGA": 0, "TCCA-TTCA": 0, "TCCA-AGGT": 0}

3. Demultiplex function

define demultiplex(R1, R2, R3, R4, index_pairs, qscore_cutoff): 
    ``` Provided four fastq files (two containing biological reads and two containing index reads), a dictionary containing all index pairs, and a qscore cutoff set by the user. Return two fastq files for each matching index-pair, two fastq files for all hopped index-pairs, two fastq files for all unknown index-pairs, and finally a tsv files with counts of all matched and hopped index-pairs ```

    unknown_count = 0
    WITH R1 open as R1, R2 open as R2, R3 open as R3, R4 open as R4: # Using gzip

        WHILE True:
            headers = read header for R1 and R4
            skip headers for R2 and R3 # readline but don't assign to variable
            R1seq, R4seq = read biological sequence from R1 and R4
            R2seq, R3seq = read index sequence from R2 and R3
            skip + in each file # readline but don't assign to variable
            qscores = read qscores for each file
            reverse_complement R3 sequence

                IF R2 quality score OR R3 quality score <= qscore cutoff:
                    open Unknown FASTQ files
                    append R1 record to Unknown_R1 file with indexes added to end of header (index1-reverse complement index2)
                    append R4 record Unknown_R4 file with indexes added to end of header (index1-reverse complement index2)
                    +1 unknown_count

                ELIF "R2_index-R3_index" not in index_pairs dictionary:
                    open Unknown FASTQ files
                    append R1 record to Unknown_R1 file with indexes added to end of header
                    append R4 record to Unknown_R4 file with indexes added to end of header
                    +1 unknown_count

                ELIF Index1_read == reverse complement of Index2_read:
                    open Index1-Index2 FASTQ files
                    append R1 record to [Index]_R1 output file with indexes added to end of header
                    append record information of R4 to [Index]_R4 output file with indexes added to end of header

                ELSE (IF Index1_read != reverse complement of Index2_read):
                    open Index-hopped FASTQ files
                    append R1 record to Hopped_R1 file with indexes added to end of header
                    append R4 record to Hopped_R4 file with indexes added to end of header

            break if R1_header is equivalent to an empty string
        Write filled index_pairs dictionary and unknown count to a index_pairs tsv
         file
        Return matched, hopped, and unknown files
        Return index_pairs tsv file

Input: TEST-input-FASTQ files
Expected output: TEST-output-FASTQ files
```

