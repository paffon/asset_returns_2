from typing import Dict, List
import pandas as pd
import yfinance as yf


def get_tickers_series(ctx: List[dict]) -> Dict[str, pd.Series]:
    result = {}

    for data_fetch_parameters in ctx:
        if not data_fetch_parameters.get('include'):
            continue
        display_name = data_fetch_parameters['display_name']
        symbol = data_fetch_parameters['symbol']
        ticker_series = get_ticker_series(symbol)
        result[display_name] = ticker_series

    return result


def get_ticker_series(ticker: str) -> pd.Series:
    ticker_history = yf.download(ticker, interval='1d')

    adj_close = ticker_history['Adj Close']

    return adj_close
