from flask import Flask, json, request
from os import path

data_folder = "data"
default_cluster = "default"
property_splitter = "="
services_config = [{
  "appName":"APOLLO-CONFIGSERVICE",
  "instanceId":"172.17.0.13:apollo-configservice:8080",
  "homepageUrl":"http://106.54.227.205:8080/"
  }]
release_key = "20210415101126-caecb751776bf468"
api = Flask(__name__)
home = path.dirname(path.abspath(__file__))

def full_file_name_of(app_id, cluster, namespace):
  return path.join(home, data_folder, app_id + "+" + cluster + "+" + namespace + ".properties")

def load_data(data, file):
  fd = open(file, "r")
  lines =fd.read().splitlines()
  fd.close()
  for line in lines:
    key_value = line.split(property_splitter, 1)
    data[key_value[0]] = key_value[1]
  return data

def load_properties(data, app_id, cluster, namespace):
  file_name = full_file_name_of(app_id, cluster, namespace)
  if path.exists(file_name):
    load_data(data, file_name)
  elif cluster != default_cluster:
    print("file not found: " + file_name)

@api.after_request
def after(response):
    print(response.get_data())
    return response

@api.route('/services/config', methods=['GET'])
def get_services_config():
  return json.dumps(services_config)

@api.route("/configs/<app_id>/<cluster>/<namespace>", methods=['GET'])
def configs(app_id, cluster, namespace):
  data = {
    "appId": app_id,
    "cluster": cluster,
    "namespaceName": namespace,
    "releaseKey": release_key 
    }
  configurations = {}
  load_properties(configurations, app_id, default_cluster, namespace)
  load_properties(configurations, app_id, cluster, namespace)
  data["configurations"] = configurations
  return json.dumps(data)

@api.route("/configfiles/json/<app_id>/<cluster>/<namespace>", methods=['GET'])
def config_files_json(app_id, cluster, namespace):
  data = {}
  load_properties(data, app_id, default_cluster, namespace)
  load_properties(data, app_id, cluster, namespace)
  return json.dumps(data)

@api.route("/notifications/v2", methods=['GET'])
def notifications():
  return request.args.get("notifications")

if __name__ == '__main__':
    api.run(threaded=True,host='0.0.0.0', port=8080)
