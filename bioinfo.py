#!/usr/bin/env python

# Author: Emma Pearce <optional@email.address>

# Check out some Python module resources:
#   - https://docs.python.org/3/tutorial/modules.html
#   - https://python101.pythonlibrary.org/chapter36_creating_modules_and_packages.html
#   - and many more: https://www.google.com/search?q=how+to+write+a+python+module

'''This module is a collection of useful bioinformatics functions
written during the Bioinformatics and Genomics Program coursework.
You should update this docstring to reflect what you would like it to say'''

__version__ = "0.4"         # Read way more about versioning here:
                            # https://en.wikipedia.org/wiki/Software_versioning

DNA_bases = "ACTGNactgn"
RNA_bases = "ACUGNacugn"

def convert_phred(letter: str) -> int:
    '''Converts a single character into a phred score'''
    return ord(letter) - 33

def qual_score(phred_score: str) -> float:
    '''Takes the phred score line and computes the average quality score of the whole string'''
    sum = 0
    for letter in phred_score:
        sum +=(convert_phred(letter))
    return(sum/len(phred_score))

def validate_base_seq(seq, RNAflag=False):
    '''This function takes a string. Returns True if string is composed
    of only As, Ts (or Us if RNAflag), Gs, Cs. False otherwise. Case insensitive.'''
    valid_bases = RNA_bases if RNAflag else DNA_bases
    return all([base in valid_bases for base in seq.upper()])

def gc_content(DNA):
    '''Returns GC content of a DNA or RNA sequence as a decimal between 0 and 1.'''
    assert validate_base_seq(DNA), "String contains invalid characters - are you sure you used a DNA sequence?"
    DNA = DNA.upper()
    return (DNA.count("G")+DNA.count("C"))/len(DNA)

def calc_median(lst: list) -> float:
    '''Given a sorted list, returns the median value of the list'''
    lst=sorted(lst)
    if len(lst) % 2 ==1: #if list has an odd number of elements
        middle_index = (len(lst) - 1)//2
        return lst[middle_index]
    else: #if list has even number of elements
        small_middle = int((len(lst) - 1)/2)
        median = (lst[small_middle] + lst[small_middle +1])/2
        return median

def oneline_fasta(file_in,file_out):
    '''Takes file_in (fasta file) that has multiple sequence lines per record
    goes through and combines all sequence lines into one'''
    with open(file_in, "r") as fi:
        with open(file_out,"w") as fo:
            line_num = 0
            for line in fi:
                line =line.strip('\n')
                if line_num == 0:
                    fo.write(f'{line}\n')
                elif line.startswith(">"):
                    fo.write(f'\n{line}\n')
                else:
                    fo.write(line)
                line_num +=1
            fo.write("\n")


if __name__ == "__main__":
    # write tests for functions above, Leslie has already populated some tests for convert_phred
    # These tests are run when you execute this file directly (instead of importing it)
    assert convert_phred("I") == 40, "wrong phred score for 'I'"
    assert convert_phred("C") == 34, "wrong phred score for 'C'"
    assert convert_phred("2") == 17, "wrong phred score for '2'"
    assert convert_phred("@") == 31, "wrong phred score for '@'"
    assert convert_phred("$") == 3, "wrong phred score for '$'"
    print("Your convert_phred function is working! Nice job")
    assert qual_score("EEE") == 36
    assert qual_score("#I") == 21
    assert qual_score("EJ") == 38.5
    print("You calcluated the correct average phred score")
    assert validate_base_seq("AATAGAT", False) == True, "Validate base seq does not work on DNA"
    assert validate_base_seq("AAUAGAU", True) == True, "Validate base seq does not work on RNA"
    assert validate_base_seq("TATUC",False) == False
    assert validate_base_seq("UCUGCU", False) == False
    print("Passed DNA and RNA tests")
    assert gc_content("GCGCGC") == 1
    assert gc_content("AATTATA") == 0
    assert gc_content("GCATCGAT") == 0.5
    print("Correctly calculated GC content")
    assert calc_median([1,2,100]) == 2, "calc_median function does not work for odd length list"
    assert calc_median([1,2]) == 1.5, "calc_median function does not work for even length list"
    assert calc_median([1,1,1,1,1,1,1,1,1,5000]) == 1
    assert calc_median([1,2,3,4,5,6,7,13]) == 4.5
    print("Median successfully calculated")
