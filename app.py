from flask import Flask, render_template

app = Flask(__name__)  # Create a Flask instance

# Define the root route which renders an HTML template
@app.route('/')
def index():
    return render_template('index.html')

# Check if the run command is executed directly (not imported)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run the app on all interfaces on port 5000
