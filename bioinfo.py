#!/usr/bin/env python

# Author: <YOU> <optional@email.address>

# Check out some Python module resources:
#   - https://docs.python.org/3/tutorial/modules.html
#   - https://python101.pythonlibrary.org/chapter36_creating_modules_and_packages.html
#   - and many more: https://www.google.com/search?q=how+to+write+a+python+module

'''This module is a collection of useful bioinformatics functions
written during the Bioinformatics and Genomics Program coursework.
You should update this docstring to reflect what you would like it to say'''

__version__ = "0.3"         # Read way more about versioning here:
                            # https://en.wikipedia.org/wiki/Software_versioning

DNA_bases = ["A","C","T","G"]
RNA_bases = ["A","C","U","G"]

def convert_phred(letter: str) -> int:
    '''Converts a single character into a phred score'''
    return ord(letter) - 33

def qual_score(phred_score: str) -> float:
    '''Converts a quality score string into an average phred score'''
    score_sum = 0
    for letter in phred_score:
        score_sum += (ord(letter)-33)
    score_avg = score_sum/len(phred_score)
    return score_avg

def validate_base_seq(seq: str, RNAflag = False) -> bool:
    '''This function takes a string. Returns True if string is composed
    of only As, Ts (or Us if RNAflag), Gs, Cs. False otherwise. Case insensitive.'''
    seq = seq.upper()
    return seq.count("A") + seq.count("U" if RNAflag else "T") + seq.count("C") + seq.count("G") == len(seq)

def gc_content(seq: str) -> float:
    '''Returns GC content of a DNA or RNA sequence as a decimal between 0 and 1.'''
    GC = seq.count("G") + seq.count("C")
    return GC/len(seq)

def calc_median(lst: list) -> float:
    '''Given a sorted list, returns the median value of the list'''
    sortedLst = sorted(lst)
    lstLen = len(lst)
    index = (lstLen - 1) // 2
    if (lstLen % 2):
        return sortedLst[index]
    else:
        return (sortedLst[index] + sortedLst[index + 1])/2.0

def oneline_fasta(input_file, output_file):
    '''docstring'''
    with open(input_file, "r") as input, open(output_file, "w") as out:
        first_line = True
        for line in input:
            if first_line ==True:
                out.write(line)
                first_line=False
            elif line[0]==">":
                out.write('\n'+line)
            else:
                line = line.strip('\n')
                out.write(line)
    return out

if __name__ == "__main__":
    # write tests for functions above, Leslie has already populated some tests for convert_phred
    # These tests are run when you execute this file directly (instead of importing it)
    assert convert_phred("I") == 40, "wrong phred score for 'I'"
    assert convert_phred("C") == 34, "wrong phred score for 'C'"
    assert convert_phred("2") == 17, "wrong phred score for '2'"
    assert convert_phred("@") == 31, "wrong phred score for '@'"
    assert convert_phred("$") == 3, "wrong phred score for '$'"
    print("Your convert_phred function is working! Nice job")

    assert qual_score("A") == 32.0, "wrong average phred score for 'A'"
    assert qual_score("AC") == 33.0, "wrong average phred score for 'AC'"
    assert qual_score("@@##") == 16.5, "wrong average phred score for '@@##'"
    assert qual_score("EEEEAAA!") == 30.0, "wrong average phred score for 'EEEEAAA!'"
    assert qual_score("$") == 3.0, "wrong average phred score for '$'"
    print("Your qual_score function is working! Nice job")

    assert validate_base_seq("AATAGAT"), "Validate base seq does not work on DNA"
    assert validate_base_seq("AAUAGAU", True), "Validate base seq does not work on RNA"
    assert validate_base_seq("R is the best!")==False, "Not a DNA string"
    assert validate_base_seq("aatagat"), "Validate base seq does not work on lowercase DNA"
    assert validate_base_seq("aauagau", True), "Validate base seq does not work on lowercase RNA"
    assert validate_base_seq("TTTTtttttTTT")
    print("Your validate_base_seq function is working! Nice job")

    assert gc_content("GCGCGC") == 1
    assert gc_content("AATTATA") == 0
    assert gc_content("GCATCGAT") == 0.5
    print("Your gc_content function is working! Nice job")

    assert calc_median([1,2,3]) == 2
    assert calc_median([5,6,7,8]) == 6.5
    assert calc_median([1,1,1,1,1,1,1,1,100]) == 1
    assert calc_median([7]) == 7
    assert calc_median([50,100]) == 75
    print("Your calc_median function is working! Nice job")

    assert oneline_fasta("test_oneline_fasta.fa", "test_oneline_fasta_output.fa")
    print("Your oneline_fasta function is working! Nice job")
