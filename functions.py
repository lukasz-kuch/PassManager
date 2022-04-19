import hashlib
import json
import os
from pickle import TRUE

def hash_password(password):
  plaintext = password.encode()
  d = hashlib.sha256(plaintext)
  hash = d.hexdigest()
  return hash

def load_json():
  with open("config.json") as json_data_file:
    return json.load(json_data_file)

def check_json():
  if os.path.isfile('config.json') and os.access('config.json', os.R_OK):
    return TRUE

def write_json(login, password):
  with open('config.json', 'w') as db_file:
    data = {
      'login': f'{login}',
      'password': f'{hash_password(password)}'
    }
    json_string = json.dumps(data)
    db_file.write(json_string)
