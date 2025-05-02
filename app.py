from flask import Flask, render_template, request, jsonify
from urllib.parse import urlparse
import tldextract

from yourscanner import scan_domain  # Replace with your scanning script

app = Flask(__name__)

# Route: Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Route: About Page (optional)
@app.route("/about")
def about():
    return render_template("about.html")

# Route: Services Page (HTML form + scan results)
@app.route("/services", methods=["GET", "POST"])
def services():
    results = None
    domain = None
    if request.method == "POST":
        domain = request.form.get("domain")
        if domain:
            results = scan_domain(domain)
    return render_template("services.html", results=results, domain=domain)

# API Endpoint: Simple GET
@app.route("/api/data", methods=["GET"])
def get_data():
    data = {"message": "Hello from Flask!"}
    return jsonify(data)

# API Endpoint: POST (JSON)
@app.route("/api/submit", methods=["POST"])
def submit_data():
    user_input = request.json.get("input")
    return jsonify({"response": f"You said: {user_input}"})

# API Endpoint: JSON-based Domain Scan
@app.route("/api/scan", methods=["POST"])
def api_scan_domain():
    data = request.get_json()
    if not data or 'domain' not in data:
        return jsonify({'error': 'No domain provided'}), 400

    domain = data['domain']

    if not is_valid_url(domain):
        return jsonify({'error': 'Invalid domain input'}), 400

    try:
        base_domain = extract_base_domain(domain)
        return jsonify({'base_domain': base_domain}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Helper Functions
def extract_base_domain(url):
    extracted = tldextract.extract(url)
    return f"{extracted.domain}.{extracted.suffix}"

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) or "." in url

# Run App
if __name__ == "__main__":
    app.run(debug=True)
