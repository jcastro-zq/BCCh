from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import re
import os

app = Flask(__name__)
API_KEY = os.environ.get("API_KEY")

@app.route('/divisas', methods=['GET'])
def get_divisas():
    key = request.args.get("key")
    if key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    url = "https://si3.bcentral.cl/indicadoressiete/secure/indicadoresdiarios.aspx"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(" ", strip=True)

    def extraer_valor(label):
        match = re.search(rf"{label}[^0-9]+([\d\.,]+)", text)
        if match:
            return float(match.group(1).replace('.', '').replace(',', '.'))
        return None

    uf = extraer_valor("Unidad de fomento")
    usd = extraer_valor("Dólar observado")

    return jsonify({"uf": uf, "usd": usd})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
