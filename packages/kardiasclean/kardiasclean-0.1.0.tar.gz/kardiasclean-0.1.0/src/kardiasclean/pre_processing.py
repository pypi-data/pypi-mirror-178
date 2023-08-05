"""Data pre-processing for ML"""
import pandas as pd
import numpy as np


def perform_binning_quantile(df: pd.DataFrame, column: str, quantile: float = 0.5, other: str = "Other") -> pd.DataFrame:
    """Bins all value counts under a given quantile value."""
    new_df = df.copy(deep=True)
    counts = new_df[column].value_counts()
    for group in counts[counts < counts.quantile(quantile)].index:
        new_df[column] = new_df[column].replace(group, other)
    return new_df[column].value_counts()


def perform_binning_scalar(df: pd.DataFrame, column: str, value: int = 2, other: str = "Other") -> pd.DataFrame:
    """Bins all value counts under a given scalar number."""
    new_df = df.copy(deep=True)
    counts = new_df[column].value_counts()
    for group in counts[counts < value].index:
        new_df[column] = new_df[column].replace(group, other)
    return new_df[column].value_counts()


def perform_matrix_encoding(column: pd.Series, group_by: pd.Series) -> pd.DataFrame:
    """Returns encoded values as a matrix of columns with binary values.

    Args:
        column (pd.Series): Column to perform the matrix on.
        group_by (pd.Series): Column to group_by, like id.

    Returns:
        pd.DataFrame: group_by column with matrix.
    """
    return pd.DataFrame(
        {
            group_by.name: group_by.values,
            **{
                f'{column.name}_{value}': np.where(column==value, 1, 0)
                for value in column.values
            }
        },
        index=column.index,
    ).groupby([group_by.name]).sum()