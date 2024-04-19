from Bio.Seq import Seq
import random

def transcribe_dna_to_rna(dna):
    result = dna.transcribe()
    return result

def translate_rna_to_protein(rna):
    result = rna.translate()
    return result

class Utility:
    @staticmethod
    def transcribe_dna_to_rna(dna):
        result = dna.transcribe()
        return result
    @staticmethod
    def translate_rna_to_protein(rna):
        result = rna.translate()
        return result
    
class SequenceStorage:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.data = {}
        return cls._instance
    #def __init__(self):
     #   self.data = {}

    def save(self, name, seq):
        self.data[name] = seq

    def read(self, name):
        return self.data[name]
    
class DNASequenceGenerator:
    alphabet = ['A','C','G','T']
    def create_sequence(self, n):
        result = ''
        for i in range(n):
            idx = random.randint(0,3)
            result = result + DNASequenceGenerator.alphabet[idx]
        return result

if __name__ == '__main__':

    sequence = 'GTGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG'
    sequence=Seq(sequence)
    rna=transcribe_dna_to_rna(sequence)
    protein=translate_rna_to_protein(rna)

    print(protein)
    sequence_name='sequence'
    storage = SequenceStorage()
    storage.save(sequence, sequence_name)
    storage1 = SequenceStorage()
    storage2 = SequenceStorage()

    print(storage1 is storage2)  # Output: True

    # Storing and retrieving data
    storage1.save("seq1", "ATCGATCG")
    print(storage2.read("seq1"))  
    random_seq= DNASequenceGenerator().create_sequence(50)
    print(random_seq)
