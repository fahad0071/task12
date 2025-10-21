from flask import Flask, request, jsonify, send_from_directory
from zeep import Client
from zeep.exceptions import Fault
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# SOAP services WSDLs
NUMBER_CONVERT_WSDL = "http://www.dataaccess.com/webservicesserver/numberconversion.wso?WSDL"
DICT_WSDL = "http://services.aonaware.com/DictService/DictService.asmx?WSDL"
TEXT_CASING_WSDL = "https://www.dataaccess.com/webservicesserver/TextCasing.wso?WSDL"
CALC_WSDL = "http://www.dneonline.com/calculator.asmx?WSDL"

# SOAP clients
number_client = Client(NUMBER_CONVERT_WSDL)
dict_client = Client(DICT_WSDL)
text_client = Client(TEXT_CASING_WSDL)
calc_client = Client(CALC_WSDL)

# Serve frontend
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')


# Number to Words
@app.route('/number-to-words', methods=['POST'])
def number_to_words():
    data = request.json
    number = int(data.get('number', 0))
    try:
        words = number_client.service.NumberToWords(number)
        return jsonify({'number': number, 'words': words})
    except Fault as fault:
        return jsonify({'error': str(fault)}), 500


# Dictionary Lookup
@app.route('/define-word', methods=['POST'])
def define_word():
    data = request.json
    word = data.get('word', '')
    try:
        results = dict_client.service.Define(word)
        definitions = []
        if results and hasattr(results, 'Definitions'):
            for item in results.Definitions:
                definitions.append(item.WordDefinition)
        return jsonify({'word': word, 'definitions': definitions})
    except Fault as fault:
        return jsonify({'error': str(fault)}), 500


# Text Casing
@app.route('/text-case', methods=['POST'])
def text_case():
    data = request.json
    text = data.get('text', '')
    case_type = data.get('case_type', 'upper').lower()
    try:
        if case_type == 'upper':
            result = text_client.service.ToUpper(text)
        elif case_type == 'lower':
            result = text_client.service.ToLower(text)
        elif case_type == 'proper':
            result = text_client.service.ToProperCase(text)
        else:
            return jsonify({'error': 'Invalid case type'}), 400
        return jsonify({'text': text, 'case_type': case_type, 'result': result})
    except Fault as fault:
        return jsonify({'error': str(fault)}), 500


# Calculator
@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    a = int(data.get('a', 0))
    b = int(data.get('b', 0))
    operation = data.get('operation', 'add').lower()
    try:
        if operation == 'add':
            result = calc_client.service.Add(a, b)
        elif operation == 'subtract':
            result = calc_client.service.Subtract(a, b)
        elif operation == 'multiply':
            result = calc_client.service.Multiply(a, b)
        elif operation == 'divide':
            result = calc_client.service.Divide(a, b)
        else:
            return jsonify({'error': 'Invalid operation'}), 400
        return jsonify({'a': a, 'b': b, 'operation': operation, 'result': result})
    except Fault as fault:
        return jsonify({'error': str(fault)}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Smart Study Helper running on http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port)
