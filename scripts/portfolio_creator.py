from datetime import datetime
from typing import Dict, Tuple, Any

import pandas as pd

from scripts.data_getter_tickers import get_tickers_series
from scripts.data_getter_crypto import get_cryptos_series


def get_portfolio(ctx) -> pd.DataFrame:
    # Get the raw data for tickers and cryptos
    df_0_raw: pd.DataFrame = get_raw_data(ctx['assets'])

    # Fill the raw data with previous value in case of missing row
    df_1_daily = fill_raw_data(df_0_raw)

    # Resample the data to the desired intervals
    df_2_periodic = periodic_resampling(df_1_daily, ctx['invest']['interval'])

    # Get data in range
    date_from = ctx['invest']['date_from']
    date_to = ctx['invest']['date_to']
    df_3_in_range = df_2_periodic.loc[date_from:date_to]

    # Fill with 0 if there's no data, implying no change
    df_4_changes = df_3_in_range.pct_change(fill_method=None)
    df_4_changes = df_4_changes.fillna(0)  # Fill missing values in the result with 0

    df_5_result = invest_money(df_4_changes, ctx)

    return df_5_result


def update_dates(ctx: dict) -> Dict[str, Any]:
    date_from_str = ctx['invest']['date_from']
    date_to_str = ctx['invest']['date_to']

    date_from_datetime = datetime.strptime(date_from_str, '%Y-%m-%d')

    if date_to_str == 'now':
        date_to_datetime = datetime.now()
    else:
        date_to_datetime = datetime.strptime(date_to_str, '%Y-%m-%d')

    ctx['invest']['date_from'] = date_from_datetime
    ctx['invest']['date_to'] = date_to_datetime

    return ctx


def get_raw_data(ctx: dict) -> pd.DataFrame:
    raw_series_data = {}
    raw_series_data.update(get_tickers_series(ctx['tickers']))
    raw_series_data.update(get_cryptos_series(ctx['cryptos']))

    result = pd.DataFrame(raw_series_data)

    if ctx.get('constant', {}).get('include'):
        # Create a series of ones with the same index as the result DataFrame
        name = ctx['constant']['display_name']
        ones_series = pd.Series(1, index=result.index, name=name)

        # Concatenate the ones_series with the result DataFrame
        result = pd.concat([ones_series, result], axis=1)

    return result


def fill_raw_data(values: pd.DataFrame) -> pd.DataFrame:
    """
    values is a DataFrame with daily datapoints, index of dtype('<M8[ns]').
    Fill missing values with the previous value.

    :param values: a pd.DataFrame of values, with index of dtype('<M8[ns]')
    :return: a pd.DataFrame of values, with index of dtype('<M8[ns]')
    """
    # Create a date range from the start to the end of the DataFrame index
    full_index = pd.date_range(start=values.index.min(), end=values.index.max(), freq='D')

    # Reindex the DataFrame to this full date range, introducing NaNs for missing dates
    values_reindexed = values.reindex(full_index)

    # Fill NaNs with the previous value
    filled_values = values_reindexed.ffill()

    return filled_values


def periodic_resampling(df: pd.DataFrame, interval: str) -> pd.DataFrame:
    """
    Resamples a daily DataFrame to a given interval.
    The DataFrame's index is of dtype('<M8[ns]').

    :param df: a pd.DataFrame of values, with index of dtype('<M8[ns]')
    :param interval: (str), "daily", "weekly" or "monthly"
    :return: a pd.DataFrame of values, with index of dtype('<M8[ns]')
    :raises ValueError: if interval is not "daily", "weekly" or "monthly"
    """

    # Use a dictionary for mapping intervals to resampling methods with proper aliases
    interval_map = {
        "day": None,
        "month": "ME",  # Resample to month-end
        "year": "Y",  # Resample to year-end
    }

    if interval not in interval_map:
        raise ValueError(f'Unknown interval {interval}')

    # Use the mapping to get the resampling method and apply it
    resample_method = interval_map.get(interval)
    if resample_method is None:
        return df  # No resampling for daily interval
    else:
        return df.resample(resample_method).last()


def invest_money(df_original, ctx) -> pd.DataFrame:
    df = df_original.copy()

    # Calculate the portfolio
    df_5_portfolio_continuous = calculate_continuous_investment(
        df, ctx['invest'])
    df_6_portfolio_lump = calculate_lump_investment(
        df, ctx['invest'])

    # Combine the two portfolios
    df_7_result = pd.concat([df_5_portfolio_continuous, df_6_portfolio_lump], axis=1)

    return df_7_result


def calculate_continuous_investment(df_original: pd.DataFrame, ctx: dict
                                    ) -> pd.DataFrame:
    """
    Calculates the portfolio value for each date in the DataFrame.

    :param df_original: a pd.DataFrame of percentage changes, with index of dtype('<M8[ns]')
    :param ctx: a dict of investment parameters
    :return: a pd.DataFrame of portfolio values, with index of dtype('<M8[ns]')
    """
    df = df_original.copy()

    initial_lump = ctx['initial_lump']
    continuous_investment = ctx['continuous_investment']

    # Initialize portfolio value with initial lump sum
    df.columns = [f'{col}_DCA' for col in df.columns]
    portfolio_values = pd.DataFrame(index=df.index, columns=df.columns)
    portfolio_values.iloc[0] = initial_lump

    # Calculate cumulative portfolio value considering continuous investments and pct changes
    for i in range(1, len(df)):
        portfolio_values.iloc[i] = (
            portfolio_values.iloc[i - 1] * (1 + df.iloc[i])
        ) + continuous_investment

    return portfolio_values


def calculate_lump_investment(df_original: pd.DataFrame, ctx: dict
                              ) -> pd.DataFrame:
    """
    Calculates the portfolio value for each date in the DataFrame as if the
    initial investment included all subsequent periodic investments.

    :param df_original: a pd.DataFrame of percentage changes, with index of dtype('<M8[ns]')
    :param ctx: a dict of investment parameters
    :return: a pd.DataFrame of portfolio values, with index of dtype('<M8[ns]')
    """
    df = df_original.copy()

    # Initial lump sum investment
    initial_lump = ctx['initial_lump']
    # Continuous investment at each time step
    continuous_investment = ctx['continuous_investment']

    # Calculate the total initial lump sum including all future investments
    total_initial_lump = initial_lump + continuous_investment * (len(df) - 1)

    # Initialize portfolio value with total initial lump sum
    df.columns = [f'{col}_lump_sum_investment' for col in df.columns]
    portfolio_values = pd.DataFrame(index=df.index, columns=df.columns)
    portfolio_values.iloc[0] = total_initial_lump

    # Calculate cumulative portfolio value considering only percentage changes
    for i in range(1, len(df)):
        portfolio_values.iloc[i] = portfolio_values.iloc[i - 1] * (1 + df.iloc[i])

    return portfolio_values
