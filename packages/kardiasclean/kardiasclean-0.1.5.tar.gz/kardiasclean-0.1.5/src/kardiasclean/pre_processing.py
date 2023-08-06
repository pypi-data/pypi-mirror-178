"""Data pre-processing for ML"""
import pandas as pd
import numpy as np
from typing import List


def perform_binning_quantile(
    df: pd.DataFrame, column: str, quantile: float = 0.5, bin_name: str = "Other"
) -> pd.DataFrame:
    """Bin low frequency values by quantile threshold.

    Args:
        df (pd.DataFrame): Dataframe.
        column (str): Column name where the values live.
        quantile (float, optional): Quantile threshold. Defaults to 0.5.
        bin_name (str, optional): Name for bin. Defaults to "Other".

    Returns:
        pd.DataFrame: Value counts of dataframe.
    """
    new_df = df.copy(deep=True)
    counts = new_df[column].value_counts()
    for group in counts[counts < counts.quantile(quantile)].index:
        new_df[column] = new_df[column].replace(group, bin_name)
    return new_df[column].value_counts()


def perform_binning_scalar(
    df: pd.DataFrame, column: str, value: int = 2, bin_name: str = "Other"
) -> pd.DataFrame:
    """Bin low frequency values by a scalar value threshold.

    Args:
        df (pd.DataFrame): Dataframe.
        column (str): Column name where the values live.
        value (int, optional): Scalar value threshold. Defaults to 2.
        bin_name (str, optional): Name for bin. Defaults to "Other".

    Returns:
        pd.DataFrame: Value counts of dataframe.
    """
    new_df = df.copy(deep=True)
    counts = new_df[column].value_counts()
    for group in counts[counts < value].index:
        new_df[column] = new_df[column].replace(group, bin_name)
    return new_df[column].value_counts()


def perform_frequency_split_quantile(
    column: pd.Series, quantile: int = 0.5
) -> List[pd.Series]:
    """Split the value counts of the data in two frequency bins, low and high, based on quantile.

    Args:
        column (pd.Series): Column to split.
        quantile (int, optional): Quantile threshold. Defaults to 0.5.

    Returns:
        Tuple[pd.Series, pd.Series]: low_frequency, high_frequency
    """
    counts = column.value_counts()
    return [
        counts[counts < counts.quantile(quantile)],
        counts[counts >= counts.quantile(quantile)],
    ]


def perform_frequency_split_scalar(
    column: pd.Series, value: int = 2
) -> List[pd.Series]:
    """Split the value counts of the data in two frequency bins, low and high, based on scalar value.

    Args:
        column (pd.Series): Column to split.
        value (int, optional): Scalar threshold. Defaults to 2.

    Returns:
        Tuple[pd.Series, pd.Series]: low_frequency, high_frequency
    """
    counts = column.value_counts()
    return [counts[counts < value], counts[counts >= value]]


def perform_matrix_encoding(column: pd.Series, group_by: pd.Series) -> pd.DataFrame:
    """Returns encoded values as a matrix of columns with binary values.

    Args:
        column (pd.Series): Column to perform the matrix on.
        group_by (pd.Series): Column to group_by, like id.

    Returns:
        pd.DataFrame: group_by column with matrix.
    """
    return (
        pd.DataFrame(
            {
                group_by.name: group_by.values,
                **{
                    f"{column.name}_{value}": np.where(column == value, 1, 0)
                    for value in column.values
                },
            },
            index=column.index,
        )
        .groupby([group_by.name])
        .sum()
        .reset_index()
    )
