# Kardiasclean

Clean, Normalize, and Tokenize medical records data.

## Install

```shell
pip install kardiasclean
```

## Usage

```python
import kardiasclean

data['surgery'] = kardiasclean.split_string(data['surgery'])
data_map = kardiasclean.spread_column(data['surgery'])

data_map['surgery'] = kardiasclean.clean_accents(data_map['surgery'])
data_map['surgery'] = kardiasclean.clean_symbols(data_map['surgery'])
data_map['keywords'] = kardiasclean.clean_stopwords(data_map['surgery'])
data_map['token'] = kardiasclean.clean_tokenize(data_map['keywords'])

list_df = kardiasclean.create_unique_list(spread_df, spread_df['token'])
list_df = list_df.drop(["patient_id", "index"], axis=1)

spread_df['surgery'] = kardiasclean.normalize_from_tokens(spread_df['token'], list_df['token'], list_df['surgery'])

>>>    patient_id                 procedure               keywords      token
>>> 0           0  Reparacion de CIA parche  cia parche reparacion  SPRXRPRSN
>>> 1           1  Reparacion de CIA parche  cia parche reparacion  SPRXRPRSN
>>> 2           2  Reparacion de CIA parche  cia parche reparacion  SPRXRPRSN
>>> 3           3  Reparacion de CIA parche  cia parche reparacion  SPRXRPRSN
>>> 4           4  Reparacion de CIA parche  cia parche reparacion  SPRXRPRSN
```

## How does it work?

This package contains ETL functions for extracting all the unique natural language medical terms from a pandas Series. The steps are much like any other ETL process for creating a bag of words/terms but this includes methods for normalizing the original column via "fuzzy string matching", preparing new DataFrames for loading to a PostgreSQL database, and ML pre-processing, binning and encoding focused on higher frequency terms.


## Development

```shell
poetry run pytest
```

## Changelog

- 0.2.0: Fixed critical 

- 0.1.7: Added support for not appending column name to matrix encoding.
- 0.1.6: Small fixes to stopwords, updated readme.
- 0.1.5: Fix stopwords implementation, added lowercase conversion.
- 0.1.3: Added Documentation.
- 0.1.2: Added SQL support and improved pre-processing functions.
- 0.1.1: Small readme fixes.
- 0.1.0: Initial Release.