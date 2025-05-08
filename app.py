from flask import Flask, request, jsonify
from db_manager import *
import time
app = Flask(__name__)

# Sample data (you can replace this with a database)
items = []

@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify(items)

@app.route('/api/items/<int:id>', methods=['GET'])
def get_item(id):
    item = next((item for item in items if item['id'] == id), None)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify(item)

@app.route('/api/items', methods=['POST'])
def create_item():
    if not request.json:
        return jsonify({'error': 'Invalid request data'}), 400
    connection = get_db_connection()
    add_item(request.json.get('name'),request.json.get('description'))
    new_item = {
        'id': len(items) + 1,
        'name': request.json.get('name'),
        'description': request.json.get('description')
    }
    items.append(new_item)
    return jsonify(new_item), 201

@app.route('/api/items/<int:id>', methods=['PUT'])
def update_item(id):
    item = next((item for item in items if item['id'] == id), None)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    
    if not request.json:
        return jsonify({'error': 'Invalid request data'}), 400
    
    item['name'] = request.json.get('name', item['name'])
    item['description'] = request.json.get('description', item['description'])
    return jsonify(item)

@app.route('/api/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = next((item for item in items if item['id'] == id), None)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    
    items.remove(item)
    return jsonify({'message': 'Item deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
