from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route('/divisas', methods=['GET'])
def get_divisas():
    url = "https://si3.bcentral.cl/indicadoressiete/secure/indicadoresdiarios.aspx"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    html_text = soup.get_text(" ", strip=True)

    def extraer_valor(label):
        match = re.search(rf"{label}[^0-9]+([\d\.,]+)", html_text)
        if match:
            return float(match.group(1).replace('.', '').replace(',', '.'))
        return None

    uf = extraer_valor("Unidad de fomento")
    usd = extraer_valor("Dólar observado")

    return jsonify({
        "uf": uf,
        "usd": usd
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
