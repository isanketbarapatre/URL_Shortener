import sqlite3
import time
from flask import Flask, request, redirect, jsonify
from datetime import datetime, timedelta
from db import init_db
from utils import create_short_url, get_analytics, get_original_url, log_access

app = Flask(__name__)
DATABASE = 'url_shortener.db'
BASE_URL = 'https://short.ly/'
DEFAULT_EXPIRY_HOURS = 24


@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.json
    original_url = data.get('url')
    expiry_hours = data.get('expiry_hours', DEFAULT_EXPIRY_HOURS)

    if not original_url:
        return jsonify({'error': 'URL is required'}), 400

    short_url = create_short_url(original_url, expiry_hours)
    return jsonify({'short_url': f'{BASE_URL}{short_url}'})

@app.route('/<short_url>', methods=['GET'])
def redirect_url(short_url):
    original_url = get_original_url(short_url)
    if original_url:
        log_access(short_url, request.remote_addr)
        return redirect(original_url)
    return jsonify({'error': 'URL not found or expired'}), 404

@app.route('/analytics/<short_url>', methods=['GET'])
def analytics(short_url):
    analytics_data = get_analytics(short_url)
    return jsonify(analytics_data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
