from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# mysql database connect
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'staging_db'
}

# API 1: query user info
@app.route('/api/users', methods=['GET'])
def get_users():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)

#API 2: add a new user
@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.get_json()
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, email) VALUES (%s, %s)", 
                   (data['username'], data['email']))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"id": new_id, "message": "User added"}), 201

if __name__ == '__main__':
    app.run(port=5000)