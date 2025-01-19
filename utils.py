from datetime import datetime, timedelta
import hashlib
import sqlite3
from db import DATABASE

# Generate a hash-based short URL
def generate_short_url(original_url):
    return hashlib.md5(original_url.encode()).hexdigest()[:6]

# Create a shortened URL
def create_short_url(original_url, expiry_hours):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Check if the URL already exists
    cursor.execute("SELECT short_url FROM urls WHERE original_url = ?", (original_url,))
    result = cursor.fetchone()
    if result:
        return result[0]

    short_url = generate_short_url(original_url)
    creation_time = datetime.now()
    expiration_time = creation_time + timedelta(hours=expiry_hours)

    cursor.execute('''
        INSERT INTO urls (original_url, short_url, creation_timestamp, expiration_timestamp)
        VALUES (?, ?, ?, ?)
    ''', (original_url, short_url, creation_time, expiration_time))
    conn.commit()
    conn.close()

    return short_url


# Fetch original URL
def get_original_url(short_url):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT original_url, expiration_timestamp FROM urls WHERE short_url = ?", (short_url,))
    result = cursor.fetchone()
    conn.close()

    if result:
        original_url, expiration_time = result
        if datetime.now() < datetime.strptime(expiration_time, '%Y-%m-%d %H:%M:%S.%f'):
            return original_url

    return None

# Log access
def log_access(short_url, ip_address):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO access_logs (short_url, access_timestamp, ip_address)
        VALUES (?, ?, ?)
    ''', (short_url, datetime.now(), ip_address))
    conn.commit()
    conn.close()

# Fetch analytics
def get_analytics(short_url):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM access_logs WHERE short_url = ?", (short_url,))
    access_count = cursor.fetchone()[0]

    cursor.execute("SELECT access_timestamp, ip_address FROM access_logs WHERE short_url = ?", (short_url,))
    access_logs = cursor.fetchall()

    conn.close()
    return {
        'access_count': access_count,
        'access_logs': [{'timestamp': log[0], 'ip_address': log[1]} for log in access_logs]
    }
