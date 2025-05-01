import os
import hashlib
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# Configuration from ENV
storage_dir = './storage'
self_addr = os.getenv('SELF_ADDR', 'node1:5000')
peers = [p for p in os.getenv('PEERS', '').split(',') if p]

# In-memory store
store = {}

# Utility: SHA-1 hashing to integer
def hash_key(key: str) -> int:
    return int(hashlib.sha1(key.encode()).hexdigest(), 16)

# Consistent-hash selection
def select_node(key: str) -> str:
    ring = sorted(peers + [self_addr])
    h = hash_key(key)
    for node in ring:
        if hash_key(node) >= h:
            return node
    return ring[0]

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'OK', 'node': self_addr})

# Phase 1: File upload & download
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'no file provided'}), 400
    path = os.path.join(storage_dir, file.filename)
    file.save(path)
    app.logger.info(f"{self_addr} saved {file.filename}")
    return jsonify({'status': 'uploaded', 'filename': file.filename})

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    app.logger.info(f"{self_addr} serving {filename}")
    return send_from_directory(storage_dir, filename)

# Phase 2 & 3: KV store with DHT routing
@app.route('/kv', methods=['POST'])
def kv_post():
    data = request.get_json() or {}
    key = data.get('key')
    val = data.get('value')
    if not key or val is None:
        return jsonify({'error': 'invalid payload'}), 400
    target = select_node(key)
    if target != self_addr:
        return requests.post(f"http://{target}/kv", json=data, timeout=2).json()
    store[key] = val
    app.logger.info(f"{self_addr} stored {key}={val}")
    return jsonify({'status': 'stored', 'key': key})

@app.route('/kv/<key>', methods=['GET'])
def kv_get(key):
    target = select_node(key)
    if target != self_addr:
        resp = requests.get(f"http://{target}/kv/{key}", timeout=2)
        return (resp.json(), resp.status_code)
    if key in store:
        return jsonify({'value': store[key]})
    return jsonify({'error': 'not found'}), 404

if __name__ == '__main__':
    os.makedirs(storage_dir, exist_ok=True)
    app.logger.info(f"Starting {self_addr}, peers: {peers}")
    app.run(host='0.0.0.0', port=5000, debug=False)