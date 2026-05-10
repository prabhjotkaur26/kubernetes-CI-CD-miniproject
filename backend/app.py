from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

@app.route('/api')
def home():
    return jsonify({
        "message": "Backend API Running Successfully!"
    })

@app.route('/health')
def health():
    return "OK"

app.run(host='0.0.0.0', port=5000)