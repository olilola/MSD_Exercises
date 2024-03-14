import argparse
import pandas as pd
import hashlib

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

def analyze_gene(filepath):

    try:
        with open(filepath, "r") as r:
            gene_count = 0
            homo_sapiens_count = 0
            gene_types = []
            element_counts = {}
            for line in r:
                gene_count += 1
                if gene_count != 1:
                            
                    parts = line.strip().split('\t')

                    if '9606' in parts[0]:  # Assuming 'tax' is the second field
                        homo_sapiens_count += 1
                    
                    gene_t = parts[9] 
                    # Check if the gene is already in the dictionary
                    if gene_t in gene_types:
                        # If it is, increment its count by 1
                        element_counts[gene_t] += 1 
                    else:
                        # If it's not, add it to the dictionary with a count of 1
                        element_counts.update({gene_t: 1})
                        gene_types.append(gene_t)
            
        max_element = max(element_counts, key=element_counts.get)
    except FileNotFoundError:
        print("Error: Input file '{}' not found.".format(filepath))
    except IOError:
        print("Error: Unable to read input file '{}'.".format(filepath))
    except Exception as e:
        print("An unexpected error occurred:", e)

    return gene_count, homo_sapiens_count, gene_types, max_element

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some strings.')
    parser.add_argument('input_file', help="Input file")
    args = parser.parse_args()
    print(args.input_file)
    md5 = calculate_md5(args.input_file)
    gene_count, homo_sapiens_count, gene_types, max_gene_type = analyze_gene(args.input_file)

    print("File md5: {}".format(md5))
    print("Answer question 1: {}".format(gene_count))
    print("Answer question 2: {}".format(homo_sapiens_count))
    print("Answer question 3: {}".format(gene_types))
    print("Answer question 4: {}".format(max_gene_type))
    
    
