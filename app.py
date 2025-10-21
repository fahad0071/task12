from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__, template_folder="templates")
CORS(app)

# Serve frontend
@app.route("/")
def index():
    return render_template("index.html")

# --- Echo Service ---
@app.route("/echo", methods=["POST"])
def echo():
    data = request.json.get("text", "")
    return jsonify({"echo": data})

# --- Credit Card Validator ---
@app.route("/validate_card", methods=["POST"])
def validate_card():
    card_number = request.json.get("card_number", "")
    is_valid = card_number.isdigit() and 13 <= len(card_number) <= 19
    return jsonify({"valid": is_valid})

# --- IP to Geo (using ip-api.com) ---
@app.route("/ip_to_geo", methods=["POST"])
def ip_to_geo():
    ip = request.json.get("ip", "")
    response = requests.get(f"http://ip-api.com/json/{ip}").json()
    return jsonify({
        "city": response.get("city", "Unknown"),
        "country": response.get("country", "Unknown"),
        "ip": ip
    })

# --- Calculator Service ---
@app.route("/calculate", methods=["POST"])
def calculate():
    expr = request.json.get("expression", "")
    try:
        result = eval(expr, {"__builtins__": {}})
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
