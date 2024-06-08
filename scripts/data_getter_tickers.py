from typing import Dict, List
import pandas as pd
import yfinance as yf


def get_tickers_series(ctx: List[dict]) -> Dict[str, pd.Series]:
    result = {}

    for ticker_data_dict in ctx:
        display_name = ticker_data_dict['display_name']
        symbol = ticker_data_dict['symbol']
        ticker_series = get_ticker_series(symbol)
        result[display_name] = ticker_series

    return result


def get_ticker_series(ticker: str) -> pd.Series:
    ticker_history = yf.download(ticker, interval='1d')

    adj_close = ticker_history['Adj Close']

    return adj_close
