# Sea URL Shortener

Sea URL Shortener is a robust yet simple Flask-based service designed to shorten URLs and collect detailed visitor metrics. It features secure API-key authenticated link creation, intelligent URL validation, and rate-limited redirects.

## 🚀 Initialization

To get started with the project, you need to set up your environment and initialize the database.

### Prerequisites
- Python 3.8+
- MySQL (for production) or SQLite (for local development)

### Step 1: Environment Setup
Clone the repository and install the dependencies:

```bash
git clone https://github.com/Sea-Rob/sea-url-shortener.git
cd sea-url-shortener
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### Step 2: Database Initialization
The project uses a custom CLI to manage the database. To initialize the database:

```bash
export FLASK_APP=app:create_app
flask setup init-db
```

This will create the necessary tables for URL mappings and visit metrics.

---

## 🛠 Functionality

The application provides two main endpoints:

### 1. Create a Short URL
- **Endpoint**: `POST /shorten`
- **Authentication**: Requires a `Bearer` token in the `Authorization` header.
- **Payload**: JSON containing the `url` to be shortened.

#### Example Request:
```bash
curl -X POST http://localhost:5000/shorten \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.google.com"}'
```

#### Example Response:
```json
{"short_id": "aB12C"}
```

### 2. Redirect to Original URL
- **Endpoint**: `GET /<short_id>`
- **Behavior**: Redirects to the original URL and logs visitor metrics.
- **Rate Limiting**: Limited to 5 requests per 5 minutes per IP address.

#### Example:
Navigating to `http://localhost:5000/aB12C` will redirect you to `https://www.google.com`.

---

## 📦 Installation & Deployment

### Local Development
To run the server locally:
```bash
export FLASK_APP=app:create_app
export API_KEY=mysupersecretkey
flask run
```

### Production Deployment
For production, it is recommended to use an ASGI-compatible server like Gunicorn with Uvicorn workers, leveraging the provided `asgi.py` wrapper.

**Environment Variables:**
| Variable | Description | Default |
| :--- | :--- | :--- |
| `FLASK_ENV` | Environment (`development`/`production`/`testing`) | `development` |
| `API_KEY` | Secret key for the `/shorten` endpoint | *Required* |
| `DB_USER` | MySQL Username | `root` |
| `DB_PASSWORD` | MySQL Password | `""` |
| `DB_HOST` | MySQL Host | `localhost` |
| `DB_NAME` | MySQL Database Name | `sea_shortener` |

**Running with Gunicorn:**
```bash
gunicorn -k uvicorn.workers.UvicornWorker asgi:app
```

---

## ⚙️ Management

The application includes a `setup` CLI group for routine management tasks.

| Command | Description |
| :--- | :--- |
| `flask setup init-db` | Initializes the database tables. |
| `flask setup drop-db` | Drops all database tables. |
| `flask setup create-db` | Used primarily for logging database status in MySQL setups. |

### Running Tests
To ensure everything is working correctly, run the test suite:
```bash
pytest
```

---

*Built with ❤️ by Sea URL Shortener Team*
