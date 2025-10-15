from flask import Flask, render_template, jsonify, request
import logging
import os

app = Flask(__name__)

# simple app metadata
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")

# logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

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
def contact():
    # Accept both JSON and form-encoded data for convenience
    data = {}
    if request.is_json:
        data = request.get_json()
    else:
        # combine form and args
        data = {**request.form.to_dict(), **request.args.to_dict()}

    name = data.get('name', 'anonymous')
    email = data.get('email', '')
    message = data.get('message', '')

    # Log the contact attempt (in production send to email/DB/queue)
    logger.info("Contact form received: name=%s email=%s message=%s", name, email, message[:200])

    return jsonify(message="Thank you, your message has been received."), 200

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # keep debug=False for parity with production; developer can set FLASK_ENV if needed
    app.run(host='0.0.0.0', port=5000)


