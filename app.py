import requests
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def fetch_crypto_data():
    # Fetch top 100 cryptocurrency data from CoinGecko API
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'per_page': 100,
        'order': 'market_cap_desc',
        'sparkline': False,
    }
    response = requests.get(url, params=params)
    data = response.json()

    # Calculate percentage decrease in price compared to ATH and add rank
    results = []
    for i, coin in enumerate(data[:100], start=1):
        name = coin['name']
        symbol = coin['symbol']
        current_price = coin['current_price']
        ath = coin['ath']
        percentage_decrease = round(((ath - current_price) / ath) * 100, 2)
        results.append({'rank': i, 'name': name, 'symbol': symbol, 'percentage_decrease': percentage_decrease})

    # Render the template with the results
    return render_template('crypto.html', results=results)

if __name__ == '__main__':
    app.run()
