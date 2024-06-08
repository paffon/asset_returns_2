import os
import pandas as pd
import matplotlib.pyplot as plt


def get_title(df):
    title = f'Portfolio- ' + ', '.join(df.columns)
    return title


def get_outputs_dir() -> str:

    current_dir = os.getcwd()
    parent_dir = os.path.dirname(current_dir)
    outputs_dir = os.path.join(parent_dir, 'outputs')

    return outputs_dir


def plot_portfolio(df: pd.DataFrame):
    """
    Creates a chart, saves it as a png, and displays it.
    :param df: the portfolio df, with index of dtype('<M8[ns]')
    """
    title = get_title(df)
    outputs_dir = get_outputs_dir()
    if not os.path.exists(outputs_dir):
        os.makedirs(outputs_dir)
    img_path = os.path.join(outputs_dir, title + '.png')

    # Plot the portfolio
    plt.figure(figsize=(10, 6))
    for column in df.columns:
        plt.plot(df.index, df[column], label=column)
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)

    # Save the plot as PNG
    plt.savefig(img_path)

    # Display the plot
    plt.show()
