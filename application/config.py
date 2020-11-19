import os
import json

path = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(path, "config.json")) as f:
    config = json.load(f)

os.environ['DB'] = config['DB']
