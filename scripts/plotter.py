import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import seaborn as sns


def get_title(df, interval):
    title = (f'Portfolio- ' + ', '.join(df.columns) +
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
    :param ctx: the context
    """
    interval = ctx['invest']['interval']

    title = get_title(df, interval)
    outputs_dir = get_outputs_dir()
    if not os.path.exists(outputs_dir):
        os.makedirs(outputs_dir)
    img_path = os.path.join(outputs_dir, make_file_name(title) + '.png')

    chart_title = make_chart_title(df)

    plot_and_save(df, chart_title, img_path)


def make_file_name(s: str):
    s = s.replace(',', '-')
    forbidden_chars = ['/', '\\', '?', '*', ':', '|', '"', '<', '>', ".", ",", "&"]
    for char in forbidden_chars:
        s = s.replace(char, '')

    s = shorten(s)
    return s


def make_chart_title(df: pd.DataFrame):
    min_date_Y_m_d = df.index.min().strftime('%Y-%m-%d')
    max_date_Y_m_d = df.index.max().strftime('%Y-%m-%d')
    title = f'Portfolio: {min_date_Y_m_d} to {max_date_Y_m_d}\n'
    title += f'Total invested amount: 100'

    return title


def shorten(s: str) -> str:
    """
    Converts a string to CamelCase, removes vowels, and removes spaces.

    :param s: the input string to be shortened
    :return: the shortened string
    """
    vowels = "aeiouAEIOU"
    # Split the string into words, capitalize the first letter of each word
    words = s.split()
    camel_case = ''.join(word.capitalize() for word in words)
    # Remove vowels
    shortened = ''.join(char for char in camel_case if char not in vowels)
    return shortened


def create_custom_legend(ax, lines, labels):
    """
    Creates a custom legend with thicker lines.

    :param ax: the Axes object to add the legend to
    :param lines: a list of Line2D objects representing the lines in the plot
    :param labels: a list of labels for the legend
    """
    # Create custom legend with thicker lines
    legend_lines = [Line2D([0], [0], color=line.get_color(), lw=4) for line in lines]
    ax.legend(handles=legend_lines, labels=labels, loc='upper left')


def plot_and_save(df: pd.DataFrame, chart_title: str, img_path: str):
    """
    Plots the portfolio values and saves the plot as an image file.

    The legend is sorted by the last value of each series in descending order.

    :param df: a pd.DataFrame of portfolio values, with index of dtype('<M8[ns]')
    :param chart_title: the title of the chart
    :param img_path: the path where the image will be saved
    """
    # Set the color palette to 'colorblind'
    sns.set_palette("colorblind")

    # Calculate the last value of each series
    last_values = df.iloc[-1].sort_values(ascending=False)
    sorted_columns = last_values.index

    # Plot the portfolio in sorted order
    plt.figure(figsize=(10, 6))
    lines = []
    for column in sorted_columns:
        line, = plt.plot(df.index, df[column], label=column)
        lines.append(line)
    plt.title(chart_title)
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.grid(True)

    # Create custom legend with thicker lines
    create_custom_legend(plt.gca(), lines, sorted_columns.tolist())

    # Save the plot as PNG
    plt.savefig(img_path)

    # Display the plot
    plt.show()
