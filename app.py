from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

# Your other service imports
# Example: import credit_card_validator, ip2geo, calculator
# You can adjust according to your actual service code

app = Flask(__name__)
CORS(app)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Echo test route
@app.route('/echo', methods=['POST'])
def echo():
    data = request.json
    return jsonify({"received": data})

# Example: Credit Card Validator API
@app.route('/validate-card', methods=['POST'])
def validate_card():
    data = request.json
    card_number = data.get('card_number')
    # Dummy validation logic
    if card_number and card_number.isdigit() and len(card_number) in [13, 16, 19]:
        return jsonify({"valid": True})
    return jsonify({"valid": False})

# Example: IP to Geo API
@app.route('/ip-geo', methods=['POST'])
def ip_geo():
    data = request.json
    ip = data.get('ip')
    # Dummy response
    return jsonify({"ip": ip, "country": "Unknown", "city": "Unknown"})

# Example: Simple Calculator API
@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    expression = data.get('expression')
    try:
        # WARNING: Using eval is dangerous in production, sanitize input!
        result = eval(expression)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)})

# Add more services here following the same pattern

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
