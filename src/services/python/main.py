import os
import json
from utils import get_traces, init_zarr

s3_url = "s3://aind-open-data/ecephys_661279_2023-03-23_15-31-18/ecephys_compressed/experiment1_Record Node 104#Neuropix-PXI-100.ProbeA.zarr/"

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def home():
    return "Traces server is <b>active</b>"


@app.route('/init', methods=['POST'])
@cross_origin()
def init():
    data = json.loads(request.data)
    return jsonify(init_zarr(**data))


@app.route('/get', methods=['POST'])
@cross_origin()
def get():
    try:
        data = json.loads(request.data)
        return jsonify(get_traces(**data))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    env_port = os.getenv('PORT')
    PORT = int(env_port) if env_port else 2020
    app.run(host='0.0.0.0', port = PORT, debug=True)