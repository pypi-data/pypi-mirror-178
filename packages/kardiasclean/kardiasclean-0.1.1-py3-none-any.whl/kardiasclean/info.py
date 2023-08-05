"""Utility functions to get insight on a DataFrame."""
import pandas as pd


def get_unique_count(df: pd.DataFrame, column: str) -> int:
    """Get the total unique values in a dataframe by column.

    Args:
        df (pd.DataFrame): Dataframe.
        column (str): Column in that dataframe.

    Returns:
        int: Count number.
    """
    return df[column].value_counts().count()


def get_difference_index(a: pd.DataFrame, b: pd.DataFrame) -> pd.DataFrame:
    """Get the index values from dataframe "a" that don't exist in dataframe "b".

    Args:
        a (pd.DataFrame): Dataframe with the most values.
        b (pd.DataFrame): Dataframe with the least values.

    Returns:
        pd.DataFrame: Index that can be used to index the original dataframe.
    """
    return list(set(a.index) - set(b.index))

