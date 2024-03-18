import argparse
import pandas as pd
import hashlib
import os

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

def read_fasta_file(file_path):
    sequences = {}
    with open(file_path, 'r') as file:
        current_header = None
        current_sequence = ''
        for line in file:
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

def validate_fasta_file(file_path):
    if not is_fasta_file(file_path):
        return "Error: Incorrect file format. File extension should be one of: '.fasta', '.fas', '.fa', '.fna', '.ffn', '.faa', '.mpfa', '.frn'."

    try:
        sequences = read_fasta_file(file_path)
        for header, sequence in sequences.items():
            if not is_valid_dna_sequence(sequence):
                return f"Error: Invalid DNA sequence in the FASTA file (sequence: {header})."
    except Exception as e:
        return f"Error: An error occurred while reading the FASTA file: {str(e)}"

    return None  # No error

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

    if not os.path.isfile(args.input_file):
        print("Error: Input file not found. Try again - usage: python gccompute.py input_file")
    else:
        md5 = calculate_md5(args.input_file)
        print("File md5: {}".format(md5))
        error_message = validate_fasta_file(args.input_file)
        if error_message:
            print(error_message)
        else:
            sequences = read_fasta_file(args.input_file)
            gc_contents = calculate_gc_content(sequences)
            for header, gc_content in gc_contents.items():
                print(f"GC-content of {header}: {gc_content:.2f}%")

    

    
    
