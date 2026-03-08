
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


import string
import random

# Dictionary to store messages per server (channel)
servers = {
    'general': [],
    'random': [],
    'help': []
}

def generate_server_code(length=6):
    chars = string.ascii_uppercase + string.digits
    while True:
        code = ''.join(random.choices(chars, k=length))
        if code not in servers:
            return code

@app.route('/servers/create', methods=['POST'])
def create_server():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    if not name:
        return jsonify({'status': 'error', 'reason': 'Server name required'}), 400
    code = generate_server_code()
    servers[code] = []
    return jsonify({'status': 'ok', 'code': code, 'name': name})

@app.route('/servers/join', methods=['POST'])
def join_server():
    data = request.get_json() or {}
    code = data.get('code', '').strip().upper()
    if code in servers:
        return jsonify({'status': 'ok', 'code': code})
    return jsonify({'status': 'error', 'reason': 'Server code not found'}), 404

@app.route('/servers', methods=['GET'])
def get_servers():
    return jsonify(list(servers.keys()))

@app.route('/messages', methods=['GET'])
def get_messages():
    server = request.args.get('server', 'general')
    if server not in servers:
        return jsonify([])
    return jsonify(servers[server])

@app.route('/messages', methods=['POST'])
def post_message():
    data = request.get_json()
    server = data.get('server', 'general')
    if server not in servers:
        return jsonify({'status': 'error', 'reason': 'Invalid server'}), 400
    if 'user' in data and 'text' in data:
        servers[server].append({'user': data['user'], 'text': data['text']})
        return jsonify({'status': 'ok'})
    return jsonify({'status': 'error', 'reason': 'Invalid data'}), 400

if __name__ == '__main__':
    app.run(debug=True)
