from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = 'your_api_key'  # Replace with your currency API key
API_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest /"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        from_currency = request.form.get('from_currency')
        to_currency = request.form.get('to_currency')
        amount = float(request.form.get('amount'))

        response = requests.get(API_URL + from_currency)
        data = response.json()

        if data['result'] == 'success':
            conversion_rate = data['conversion_rates'][to_currency]
            converted_amount = round(amount * conversion_rate, 2)
            return render_template('index.html', converted_amount=converted_amount, from_currency=from_currency, to_currency=to_currency)
        else:
            return render_template('index.html', error="Error in fetching data. Please try again.")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
