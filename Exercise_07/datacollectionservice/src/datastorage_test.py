import unittest

import datastorage

class TestDataStorage(unittest.TestCase):

    def test_create_patient(self):
        ds = datastorage.DataStorage()
        result = ds.create_patient("David Herzig")
        self.assertTrue(result >= 0)

    def test_create_experiments(self):
        ds = datastorage.DataStorage()
        result = ds.create_experiment("test")    
        #self.assertTrue(result.is_integer())
        self.assertTrue(result >= 0)

if __name__ == '__main__':
    unittest.main()
