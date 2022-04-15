import hashlib
import json

def hash_password(password):
  plaintext = password.encode()
  d = hashlib.sha256(plaintext)
  hash = d.hexdigest()
  return hash

def load_json():
  with open("config.json") as json_data_file:
    return json.load(json_data_file)

def write_json(login, password):
  with open("config.json") as json_data_file:
    data =  json.load(json_data_file)
    data['login'] = login
    data['password'] = hash_password(password)
  with open('config.json', 'w') as json_data_file:
    json.dump(data, json_data_file)
