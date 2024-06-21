from Bio.Seq import Seq
import random

# (2) Create a utility class, which contains both methods as static methods
class SequenceUtils:
    
    @staticmethod
    def transcribe_dna_to_rna(dna):
        result = dna.transcribe()
        return result

    @staticmethod
    def translate_rna_to_protein(rna):
        result = rna.translate()
        return result

class SequenceStorage:
    # (4) Change the class SequenceStorage in a way that only one object could exist. Done with Singleton design pattern.
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SequenceStorage, cls).__new__(cls, *args, **kwargs)
            cls._instance.data = {}
        return cls._instance

    def save(self, name, seq):
        self.data[name] = seq

    def read(self, name):
        return self.data.get(name)

class DNASequenceGenerator:
    alphabet = ['A','C','G','T']
    
    def create_sequence(self, n):
        return ''.join(random.choice(DNASequenceGenerator.alphabet) for _ in range(n))

class ProteinSequenceGenerator:
    # represent the 20 standard amino acids found in proteins
    alphabet = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
    
    def create_sequence(self, n):
        return ''.join(random.choice(ProteinSequenceGenerator.alphabet) for _ in range(n))

class SequenceFactory:
    
    @staticmethod
    def create_sequence(sequence_type, length):
        if sequence_type == 'DNA':
            return DNASequenceGenerator().create_sequence(length)
        elif sequence_type == 'Protein':
            return ProteinSequenceGenerator().create_sequence(length)
        else:
            raise ValueError("Invalid sequence type. Choose 'DNA' or 'Protein'.")

if __name__ == '__main__':
 
    sequence = 'GTGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG'
    dna_seq = Seq(sequence)

    # (1) Translate the given DNA sequence into a protein sequence
    rna_seq = SequenceUtils.transcribe_dna_to_rna(dna_seq)
    protein_seq = SequenceUtils.translate_rna_to_protein(rna_seq)

    # (3) Store the sequence into an object of the class SequenceStorage
    storage = SequenceStorage()
    storage.save('Original DNA', dna_seq)
    storage.save('Transcribed RNA', rna_seq)
    storage.save('Translated Protein', protein_seq)

    print("Stored sequences:")
    for name, seq in storage.data.items():
        print(f"{name}: {seq}")

    # (5) Create a random sequence with the DNASequenceGenerator
    random_dna_sequence = DNASequenceGenerator().create_sequence(10)
    print("Random DNA Sequence:", random_dna_sequence)
    
    # (6) Extend to work with protein sequences (already integrated in ProteinSequenceGenerator)

    # (7) Create a sequence using SequenceFactory
    random_protein_sequence = SequenceFactory.create_sequence('Protein', 10)
    print("Random Protein Sequence:", random_protein_sequence)
