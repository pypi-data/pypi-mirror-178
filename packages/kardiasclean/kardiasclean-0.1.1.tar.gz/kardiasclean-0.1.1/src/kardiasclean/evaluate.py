"""Evaluate results."""
import pandas as pd


def evaluate_distribution(high_frequency: pd.Series, low_frequency: pd.Series):
    n_other = low_frequency.sum()
    n_top = high_frequency.sum()
    count_top = high_frequency.count()
    total = n_other + n_top
    return (
        f"Number of high frequency data: {n_top}\n"
        f"Number of low frequency data: {n_other}\n"
        f"{'-'*20}\n"
        f"Total Number of data: {total}.\n"
        f"Percentage of high data: {100*n_top/total:.2f}%\n"
        f"Percentage of low data: {100*n_other/total:.2f}%\n"
        f"{'-'*20}\n"
        f"Summary\n"
        f"{'-'*20}\n"
        f"From {total} data, {count_top} account for {100*n_top/total:.2f}% of the total count.\n"
    )