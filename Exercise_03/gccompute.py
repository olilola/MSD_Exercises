import argparse
import pandas as pd
import hashlib
import os
from io import BytesIO

def main(input_item, type):
    #print(input_item)
    if type == 'file':
        # Process the uploaded file
        if not os.path.isfile(input_item):
            return "Error: Input file not found. Try again - usage: python gccompute.py input_file"
        
        if not is_fasta_file(input_item):
            return "Error: Incorrect file format. File extension should be one of: '.fasta', '.fas', '.fa', '.fna', '.ffn', '.faa', '.mpfa', '.frn'."

        try:
            sequences = read_fasta_file(input_item)
        except Exception as e:
            return f"Error: An error occurred while reading the FASTA file: {str(e)}"

        md5 = calculate_md5(input_item)
        print("File md5: {}".format(md5))

    elif type == 'text':
        sequences = input_item

    else:
        return "Input not recognized. Try again"



    error_message = validate_fasta(sequences)
    if error_message:
        return error_message

    gc_contents = calculate_gc_content(sequences)
    for header, gc_content in gc_contents.items():
        print(f"GC-content of {header}: {gc_content:.2f}%")

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

def read_fasta_file(text):
    sequences = {}
    
    current_header = None
    current_sequence = ''
    for line in text:
        line = line.strip()
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
    return sequences


def is_valid_dna_sequence(sequence):
    valid_chars = set('ACGT')
    return all(base in valid_chars for base in sequence)

def is_fasta_file(file_path):
    valid_extensions = ['.fasta', '.fas', '.fa', '.fna', '.ffn', '.faa', '.mpfa', '.frn']
    _, extension = os.path.splitext(file_path)
    return extension.lower() in valid_extensions

def validate_fasta(sequences):
    #print(sequence)
    for header, sequence in sequences.items():
        if not is_valid_dna_sequence(sequence):
            return f"Error: Invalid DNA sequence in the FASTA file (sequence: {header})."
    
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
    main(args.input_file, type="file")

    

    

    
    
