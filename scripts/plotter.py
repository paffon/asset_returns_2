import os
import pandas as pd
import matplotlib.pyplot as plt


def get_title(df,initial, periodic_addition, interval):
    title = (f'Portfolio- ' + ', '.join(df.columns) +
             f' - Initial: {initial}, Periodic: {periodic_addition}' +
             f' Interval: {interval}')
    return title


def get_outputs_dir() -> str:

    current_dir = os.getcwd()
    parent_dir = os.path.dirname(current_dir)
    outputs_dir = os.path.join(parent_dir, 'outputs')

    return outputs_dir


def plot_portfolio(df: pd.DataFrame, ctx):
    """
    Creates a chart, saves it as a png, and displays it.
    :param df: the portfolio df, with index of dtype('<M8[ns]')
    """
    initial = ctx['invest']['initial_lump']
    periodic_addition = ctx['invest']['continuous_investment']
    interval = ctx['invest']['interval']

    title = get_title(df, initial, periodic_addition, interval)
    outputs_dir = get_outputs_dir()
    if not os.path.exists(outputs_dir):
        os.makedirs(outputs_dir)
    img_path = os.path.join(outputs_dir, strip_forbidden_chars(title) + '.png')

    chart_title = make_chart_title(df, initial, periodic_addition, interval)

    plot_and_save(df, chart_title, img_path)


def strip_forbidden_chars(s: str):
    s = s.replace(',', '-')
    forbidden_chars = ['/', '\\', '?', '*', ':', '|', '"', '<', '>', ".", ",", "&"]
    for char in forbidden_chars:
        s = s.replace(char, '')
    return s


def make_chart_title(df: pd.DataFrame, initial, periodic_addition, interval):
    min_date_Y_m_d = df.index.min().strftime('%Y-%m-%d')
    max_date_Y_m_d = df.index.max().strftime('%Y-%m-%d')
    title = f'Portfolio worth from {min_date_Y_m_d} to {max_date_Y_m_d}'
    title += '\n' + ', '.join(df.columns) + '\n'
    title += f'Initial: {initial}, added every {interval}: {periodic_addition}'

    return title


def plot_and_save(df, chart_title, img_path):
    # Plot the portfolio
    plt.figure(figsize=(10, 6))
    for column in df.columns:
        plt.plot(df.index, df[column], label=column)
    plt.title(chart_title)
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend(loc='upper left')
    plt.grid(True)

    # Save the plot as PNG
    plt.savefig(img_path)

    # Display the plot
    plt.show()
