import argparse
import pandas as pd
import hashlib
import os
from io import BytesIO

def main(input_item):

    sequences = read_fasta_file(input_item)

    error_message = validate_fasta(sequences)
    if error_message:
        return error_message

    gc_contents = calculate_gc_content(sequences)

    return gc_contents

class ValidationException(Exception):
    pass

def calculate_md5(file_path):
    # Open the file in binary mode
    with open(file_path, "rb") as f:
        # Initialize the MD5 hash object
        md5_hash = hashlib.md5()
        
        # Read the file in chunks to efficiently handle large files
        while chunk := f.read(4096):
            # Update the hash object with the bytes from the file chunk
            md5_hash.update(chunk)
    
    # Get the hexadecimal representation of the MD5 hash
    md5_hex = md5_hash.hexdigest()
    
    return md5_hex

def read_fasta_file(input):
    sequences = {}
    
    current_header = None
    current_sequence = ''
    
    #Check if file and decode
    if type(input) == bytes:
        text = input.decode('utf-8')
        file = True
    else:
        text = input
        file = False

    for line in text.splitlines():

        
        if line.startswith('>'):
            if current_header is not None:
                sequences[current_header] = current_sequence
            current_header = line[1:]
            current_sequence = ''
        else:
            current_sequence += line
    # Add the last sequence after the loop ends
    if current_header is not None:
        sequences[current_header] = current_sequence
    else:
        sequences['Single sequence'] = current_sequence
    return sequences


def is_valid_dna_sequence(sequence):
    valid_chars = set('ACGT')
    return all(base in valid_chars for base in sequence)


def validate_fasta(sequences):

    for header, sequence in sequences.items():
        if not is_valid_dna_sequence(sequence):
            raise ValidationException("Invalid FASTA file: Invalid sequence.")
    
    return None

def calculate_gc_content(sequences):
    gc_contents = {}
    for header, dna_sequence in sequences.items():
        gc_count = dna_sequence.count('G') + dna_sequence.count('C')
        total_bases = len(dna_sequence)
        gc_content = (gc_count / total_bases) * 100
        gc_contents[header] = gc_content
    return gc_contents

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Usage: python gccompute.py input_file')
    parser.add_argument('input_file', help="Input file")
    args = parser.parse_args()
    main(args.input_file)

    

    

    
    
