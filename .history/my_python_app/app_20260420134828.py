from flask import Flask, render_template, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
import os

app = Flask(__name__)

# simple app metadata
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

# logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# rate limiting (in-memory; swap to Redis for multi-pod consistency)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per minute"],
    storage_uri="memory://",
)


@app.after_request
def set_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "style-src 'self' 'unsafe-inline' https://stackpath.bootstrapcdn.com; "
        "script-src 'self' 'unsafe-inline' https://code.jquery.com https://cdn.jsdelivr.net https://stackpath.bootstrapcdn.com; "
        "img-src 'self' https://picsum.photos https://fastly.picsum.photos data:; "
        "font-src 'self' https://stackpath.bootstrapcdn.com; "
        "connect-src 'self'"
    )
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify(status='ok'), 200

@app.route('/api/version')
def version():
    return jsonify(version=APP_VERSION), 200

@app.route('/contact', methods=['POST'])
@limiter.limit("5 per minute")
def contact():
    # Accept both JSON and form-encoded data for convenience
    data = {}
    if request.is_json:
        data = request.get_json(silent=True) or {}
    else:
        data = {**request.form.to_dict(), **request.args.to_dict()}

    name = (data.get('name') or 'anonymous').strip()[:100]
    email = (data.get('email') or '').strip()[:254]
    message = (data.get('message') or '').strip()[:2000]

    if not message:
        return jsonify(error="Message is required."), 400

    # Log the contact attempt (in production send to email/DB/queue)
    logger.info("Contact form received: name=%s email=%s message=%s", name, email, message[:200])

    return jsonify(message="Thank you, your message has been received."), 200

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # keep debug=False for parity with production; developer can set FLASK_ENV if needed
    app.run(host='0.0.0.0', port=5000)


