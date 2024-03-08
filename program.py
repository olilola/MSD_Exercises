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

def read_the_file(input_file):
    try:
        df = pd.read_csv(input_file, delimiter='\t')
        return df
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: File '{input_file}' is empty.")
        return None
    except pd.errors.ParserError:
        print(f"Error: Unable to parse file '{input_file}'.")
        return None

def count_genes(df):
    # Select the column you want to count records from
    selected_column = 'GeneID'  # Replace 'column_name' with the name of your column
    # Get the number of unique values in the column
    unique_values_count = len(df[selected_column].unique())
    print("Answer question 1: {}".format(unique_values_count))

def gene_homo_sapiens(df):
    selected_column = '#tax_id'  # Replace 'column_name' with the name of your column
    # Get the number of unique values in the column
    #["9606"]
    count = (df[selected_column] == 9606).sum()
    print("Answer question 2: {}".format(count))

def gene_type_data(df):
    # Select the column you want to extract unique strings from
    selected_column = 'type_of_gene'  # Replace 'column_name' with the name of your column
    # Get the unique strings from the column
    unique_strings = df[selected_column].unique()
    #count repetitions
    # Count the occurrences of each unique string in the column
    string_counts = df[selected_column].value_counts()
    # Find the string that repeated the most
    most_repeated_string = string_counts.idxmax()
    # Print the array of unique strings
    print("Answer question 3: ")
    print(unique_strings)
    print("Answer question 4: {}".format(most_repeated_string))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some strings.')
    parser.add_argument('input_file', help="Input file")
    
    args = parser.parse_args()
    
    md5_hash = calculate_md5(args.input_file)
    
    print("MD5 hash of the file:", md5_hash)
    df = read_the_file(args.input_file)
    count_genes(df)
    gene_homo_sapiens(df)
    gene_type_data(df)
    #add the wrong extension file and return an error