from typing import Dict, List
import pandas as pd
import requests


def get_cryptos_series(ctx: List[dict]) -> Dict[str, pd.Series]:
    result = {}

    for ticker_data_dict in ctx:
        display_name = ticker_data_dict['display_name']
        symbol = ticker_data_dict['symbol']
        crypto_series = get_crypto_series(symbol)
        result[display_name] = crypto_series

    return result


def get_crypto_series(symbol: str) -> pd.Series:
    # API request to fetch data
    url = construct_url(symbol)
    response = requests.get(url)
    response_json = response.json()
    data = response_json['prices']

    # Convert the time from milliseconds to datetime and create a DataFrame
    df = pd.DataFrame(data, columns=['time', 'price'])
    df['time'] = pd.to_datetime(df['time'], unit='ms')

    # Set 'time' column as index and resample to get one price per day (using
    # the last entry of each day)
    df.set_index('time', inplace=True)
    series = df.resample('D').last()['price']

    # Assign name to the series
    series.name = 'prices'

    return series


def construct_url(symbol: str) -> str:

    base = 'https://api.coingecko.com/api/v3/coins/'
    params = f'market_chart?vs_currency=usd&interval=daily&days=365'
    url = f'{base}{symbol}/{params}'

    return url
