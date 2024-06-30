import datastorage
import tracemalloc
import psutil
import os
import logging

import json
from flask import request, Flask
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

class Experiment:
  def __init__(self, id, name):
    self.id = id
    self.name = name

def to_json(obj):
  return json.dumps(obj, default=lambda obj: obj.__dict__)

@app.route('/info', methods=['GET'])
def index():
    return json.dumps({'application' : 'Data Collection Service',
    'author' : 'David Herzig', 'version' : 'v1_0_0', 'Support' : 'dave.herzig@gmail.com'})

@app.route('/experiment', methods=['POST', 'GET'])
def experiment_action():
  ds = datastorage.DataStorage()
  assert ds is not None
  if request.method == 'POST':
    logging.info("Endpoint /experiment POST called")
    form_data = request.data
    logging.debug(f"Received form data: {form_data}")
    data = json.loads(form_data)
    id = ds.create_experiment(data['name'])
    logging.info(f"Created experiment with ID: {id}")
    return json.dumps({'result' : id})
  if request.method == 'GET':
    logging.info("Endpoint /experiment GET called")
    exps = ds.get_experiments()
    exps_array = []
    for key, value in exps.items():
      exp = Experiment(key, value)
      exps_array.append(exp)
    return to_json(exps_array)
  
@app.route('/patient', methods=['POST', 'GET'])
def patient_action():
  ds = datastorage.DataStorage()
  assert ds is not None
  if request.method == 'POST':
    logging.info("Endpoint /patient POST called")
    form_data = request.data
    logging.debug(f"Received form data: {form_data}")
    data = json.loads(form_data)
    id = ds.create_patient(data['name'])
    logging.info(f"Created patient with ID: {id}")
    return json.dumps({'result' : id})
  if request.method == 'GET':
    logging.info("Endpoint /patient GET called")
    return ds.get_patients()
  
  
@app.route('/store', methods=['POST'])
def store_data():
  ds = datastorage.DataStorage()
  assert ds is not None
  form_data = request.data
  data = json.loads(form_data)
  filename = data['filename']
  type = data['type']

  assert type in ['experiments', 'patients', 'data'], f"Invalid data type: {type}"
  
  if type == 'experiments':
    ds.store_experiments(filename)
  elif type == 'patients':
    ds.store_patients(filename)
  elif type == 'data':
    ds.store_data(filename)
  else:
    logging.error(f"Invalid data type received: {type}")
    print('invalid data type: ' + type)
    
  return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

  
@app.route('/data', methods=['POST'])
def upload_data():
  form_data = request.data
  print(form_data)
  data = json.loads(form_data)
  ds = datastorage.DataStorage()
  ds.add_data(data)

  return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
  

if __name__ == '__main__':
  logging.info("Starting Flask application")
  app.run(debug=True, host="0.0.0.0", port=8080)
  #app.run(debug=True, port=8080)
  
