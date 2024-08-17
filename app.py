from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = 'your_api_key'  # Replace with your currency API key
API_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"

def get_supported_currencies():
    response = requests.get(API_URL + "USD")
    data = response.json()
    if data['result'] == 'success':
        return data['conversion_rates'].keys()
    return []

@app.route('/', methods=['GET', 'POST'])
def index():
    currencies = get_supported_currencies()
    if request.method == 'POST':
        from_currency = request.form.get('from_currency')
        to_currency = request.form.get('to_currency')
        amount = float(request.form.get('amount'))

        response = requests.get(API_URL + from_currency)
        data = response.json()

        if data['result'] == 'success':
            conversion_rate = data['conversion_rates'][to_currency]
            converted_amount = round(amount * conversion_rate, 2)
            return render_template('index.html', converted_amount=converted_amount, from_currency=from_currency, to_currency=to_currency, currencies=currencies)
        else:
            return render_template('index.html', error="Error in fetching data. Please try again.", currencies=currencies)
    return render_template('index.html', currencies=currencies)

if __name__ == '__main__':
    app.run(debug=True)
