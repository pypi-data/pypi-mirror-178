"""Utility functions to get insight on a DataFrame."""
import pandas as pd


def get_unique_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Get the total unique values in all columns.

    Args:
        df (pd.DataFrame): Column.

    Returns:
        int: Count number.
    """
    unique = pd.DataFrame(
        {column: df[column].value_counts().count() for column in df.columns},
        index=["unique_count"],
    )
    percent = (unique / df.count()).rename(index={"unique_count": "percent_of_total"})
    per = (1 / percent).rename(index={"percent_of_total": "avg_per_record"})
    return pd.concat(
        [
            unique,
            percent,
            per,
        ]
    )


def get_difference_index(a: pd.DataFrame, b: pd.DataFrame) -> pd.DataFrame:
    """Get the index values from dataframe "a" that don't exist in dataframe "b".

    Args:
        a (pd.DataFrame): Dataframe with the most values.
        b (pd.DataFrame): Dataframe with the least values.

    Returns:
        pd.DataFrame: Index that can be used to index the original dataframe.
    """
    return list(set(a.index) - set(b.index))
