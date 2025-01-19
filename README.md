# URL_Shortener

This project is a Python-based URL shortener system built with Flask. It shortens URLs, tracks usage analytics, and supports link expiration.

## Features

### 1. Core Functionality
- Create a shortened URL for any long URL.
- Each shortened URL is unique and includes a base URL (e.g., `https://short.ly/abc123`).

### 2. Expiry
- Users can specify an expiration time for the shortened URL in hours.
- If no expiration time is provided, the default is 24 hours.
- Expired URLs will not redirect to the original URL.

### 3. Analytics
- Tracks the number of times a shortened URL is accessed.
- Logs access timestamps and IP addresses.

### 4. Storage
- Uses SQLite to store:
  - Original URL.
  - Shortened URL.
  - Creation timestamp.
  - Expiration timestamp.
  - Access logs (shortened URL, timestamp, IP address).

### 5. API Endpoints

#### POST `/shorten`
**Description:** Create a shortened URL.

- **Request Body:**
  ```json
  {
      "url": "https://example.com",
      "expiry_hours": 48
  }
  ```
- **Response:**
  ```json
  {
      "short_url": "https://short.ly/abc123"
  }
  ```

#### GET `/<short_url>`
**Description:** Redirect to the original URL if the link is not expired.

- **Response:**
  - Redirects to the original URL if valid.
  - Returns an error if the URL is expired or not found:
    ```json
    {
        "error": "URL not found or expired"
    }
    ```

#### GET `/analytics/<short_url>`
**Description:** Retrieve analytics data for a specific shortened URL.

- **Response:**
  ```json
  {
      "access_count": 10,
      "access_logs": [
          {
              "timestamp": "2025-01-19 10:00:00",
              "ip_address": "127.0.0.1"
          },
          {
              "timestamp": "2025-01-19 10:05:00",
              "ip_address": "127.0.0.1"
          }
      ]
  }
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/url-shortener.git
   cd url-shortener
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```bash
   python init_db.py
   ```

5. Run the Flask server:
   ```bash
   python url_shortener.py
   ```

## Testing

### Create a Shortened URL
Use the `POST /shorten` endpoint to generate a shortened URL:
```bash
curl -X POST http://127.0.0.1:5000/shorten \
-H "Content-Type: application/json" \
-d '{"url": "https://example.com", "expiry_hours": 48}'
```

### Redirect to Original URL
Use the `GET /<short_url>` endpoint to test redirection:
```bash
curl -i http://127.0.0.1:5000/abc123
```

### Retrieve Analytics
Use the `GET /analytics/<short_url>` endpoint:
```bash
curl http://127.0.0.1:5000/analytics/abc123
```

## Notes

- Ensure that the Flask server is running before making API requests.
- Modify the `BASE_URL` variable in the code to set your custom domain for shortened URLs.

## Future Enhancements

- Add user authentication for managing URLs.
- Implement rate-limiting to prevent abuse.
- Add support for password-protected URLs.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

