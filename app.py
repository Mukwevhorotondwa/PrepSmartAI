from flask import Flask, request, jsonify
from db_manager import *

app = Flask(__name__)

# Initialize database when the app starts
initialize_db()

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        users = get_all_items_from_db()
        if not users:
            return jsonify({'message': 'No users found'}), 404
        return jsonify(users)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/by-name/<string:name>', methods=['GET'])
def get_user_by_name(name):
    try:
        user = get_item_from_db(name)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/by-id/<int:id>', methods=['GET'])
def get_user_by_id(id):
    try:
        user = get_item_from_db_by_id(id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users', methods=['POST'])
def create_user():
    if not request.json or 'name' not in request.json or 'description' not in request.json:
        return jsonify({'error': 'Invalid request data'}), 400
    try:
        new_user = add_item(request.json['name'], request.json['description'])
        return jsonify(new_user), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    if not request.json:
        return jsonify({'error': 'Invalid request data'}), 400
    try:
        updated_user = update_item(id, request.json.get('name'), request.json.get('description'))
        if not updated_user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(updated_user)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        success = delete_item_from_db(id)
        if not success:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'message': 'User deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8009)