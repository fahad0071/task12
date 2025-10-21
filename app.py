from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Serve index.html
@app.route("/")
def home():
    return render_template("index.html")

# Echo API
@app.route("/echo", methods=["POST"])
def echo():
    data = request.json.get("message", "")
    return jsonify({"echo": data})

# Credit Card Validator (simple Luhn check)
@app.route("/validate-card", methods=["POST"])
def validate_card():
    card_number = request.json.get("card_number", "")
    def luhn_check(card_num):
        total = 0
        reverse_digits = card_num[::-1]
        for i, digit in enumerate(reverse_digits):
            n = int(digit)
            if i % 2 == 1:
                n *= 2
                if n > 9:
                    n -= 9
            total += n
        return total % 10 == 0
    is_valid = luhn_check(card_number) if card_number.isdigit() else False
    return jsonify({"valid": is_valid})

# IP to Geo API
@app.route("/ip-geo", methods=["POST"])
def ip_geo():
    ip = request.json.get("ip", "")
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,query")
        data = response.json()
        if data.get("status") != "success":
            return jsonify({"ip": ip, "city": "Unknown", "country": "Unknown"})
        return jsonify({"ip": data.get("query"), "city": data.get("city"), "country": data.get("country")})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Calculator API
@app.route("/calculate", methods=["POST"])
def calculate():
    expr = request.json.get("expression", "")
    try:
        # Only allow safe characters
        allowed_chars = "0123456789+-*/(). "
        if not all(c in allowed_chars for c in expr):
            raise ValueError("Invalid characters")
        result = eval(expr)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
