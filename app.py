from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

API_KEY = "mi_clave_ultra_secreta_123"

@app.route('/divisas', methods=['GET'])
def get_divisas():
    key = request.args.get("key")
    if key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    url = "https://si3.bcentral.cl/indicadoressiete/secure/indicadoresdiarios.aspx"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    html_text = soup.get_text(" ", strip=True)

    def extraer_valor(label):
        match = re.search(rf"{label}[^0-9]+([\d\.,]+)", html_text)
        if match:
            return float(match.group(1).replace('.', '').replace(',', '.')
