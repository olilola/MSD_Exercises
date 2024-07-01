import json
import logging
import os
import tracemalloc
import psutil

from flask import request, Flask
import datastorage

app = Flask(__name__)

class Experiment:
    """Class representing an experiment with an ID and name."""
    
    def __init__(self, exp_id, name):
        self.exp_id = exp_id
        self.name = name

def to_json(obj):
    """Convert an object to JSON string."""
    return json.dumps(obj, default=lambda o: o.__dict__)

@app.route('/info', methods=['GET'])
def index():
    """Return information about the Data Collection Service."""
    return json.dumps({
        'application': 'Data Collection Service',
        'author': 'David Herzig',
        'version': 'v1_0_0',
        'Support': 'dave.herzig@gmail.com'
    })

@app.route('/experiment', methods=['POST', 'GET'])
def experiment_action():
    """Handle POST and GET requests for experiments."""
    ds = datastorage.DataStorage()
    assert ds is not None
    if request.method == 'POST':
        logging.info("Endpoint /experiment POST called")
        form_data = request.data
        logging.debug("Received form data: %s", form_data)
        data = json.loads(form_data)
        exp_id = ds.create_experiment(data['name'])
        logging.info("Created experiment with ID: %s", exp_id)
        return json.dumps({'result': exp_id})
    if request.method == 'GET':
        logging.info("Endpoint /experiment GET called")
        experiments = ds.get_experiments()
        experiments_list = [
            Experiment(key, value) for key, value in experiments.items()
        ]
        return to_json(experiments_list)

@app.route('/patient', methods=['POST', 'GET'])
def patient_action():
    """Handle POST and GET requests for patients."""
    ds = datastorage.DataStorage()
    assert ds is not None
    if request.method == 'POST':
        logging.info("Endpoint /patient POST called")
        form_data = request.data
        logging.debug("Received form data: %s", form_data)
        data = json.loads(form_data)
        patient_id = ds.create_patient(data['name'])
        logging.info("Created patient with ID: %s", patient_id)
        return json.dumps({'result': patient_id})
    if request.method == 'GET':
        logging.info("Endpoint /patient GET called")
        return ds.get_patients()

@app.route('/store', methods=['POST'])
def store_data():
    """Store data based on the type specified in the request."""
    ds = datastorage.DataStorage()
    assert ds is not None
    form_data = request.data
    data = json.loads(form_data)
    filename = data['filename']
    data_type = data['type']

    assert data_type in ['experiments', 'patients', 'data'], f"Invalid data type: {data_type}"
    
    if data_type == 'experiments':
        ds.store_experiments(filename)
    elif data_type == 'patients':
        ds.store_patients(filename)
    elif data_type == 'data':
        ds.store_data(filename)
    else:
        logging.error("Invalid data type received: %s", data_type)
        return json.dumps({'error': 'invalid data type'}), 400

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

@app.route('/data', methods=['POST'])
def upload_data():
    """Upload data to the data storage."""
    form_data = request.data
    data = json.loads(form_data)
    ds = datastorage.DataStorage()
    ds.add_data(data)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting Flask application")
    app.run(debug=True, host="0.0.0.0", port=8080)