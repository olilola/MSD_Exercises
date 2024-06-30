import json
import idgenerator
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("datastorage.log"),
        logging.StreamHandler()
    ]
)

class DataPoint(object):
    def __init__(self, patient_id, experiment_id, data):
        self.id = idgenerator.generate_unique_identifier()
        self.patient_id = patient_id
        self.experiment_id = experiment_id
        self.data = data

class DataStorage(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DataStorage, cls).__new__(cls)
            cls.instance.experiments = {}
            cls.instance.patients = {}
            cls.instance.data = []
            logging.debug("DataStorage instance created")
        return cls.instance
    
    def create_patient(self, name):
        id = len(self.patients)
        logging.debug(f"New Patient ID: {id}")
        self.patients[id] = name
        return id
    
    def create_experiment(self, name):
        id = len(self.experiments)
        self.experiments[id] = name
        return id
    
    def get_patients(self):
        return self.patients
    
    def get_experiments(self):
        return self.experiments
    
    def add_data(self, dataobj):
        self.data.append(dataobj)

    def store_data(self, filename):
        # store data into file
        self.store(filename, self.data)
        self.data.clear()
    
    def store_patients(self, filename):
        self.store(filename, self.patients)
    
    def store_experiments(self, filename):
        self.store(filename, self.experiments)
    
    def store(self, filename, data):
        json_object = json.dumps(data, indent=4)
        with open(filename + ".json", "w") as outfile:
            outfile.write(json_object)

# Example usage to generate logs
if __name__ == "__main__":
    ds = DataStorage()
    patient_id = ds.create_patient("Ola")
    experiment_id = ds.create_experiment("Experiment 1")
    data_point = DataPoint(patient_id, experiment_id, {"value": 42})
    ds.add_data(data_point)
    ds.store_data("data")
    ds.store_patients("patients")
    ds.store_experiments("experiments")
