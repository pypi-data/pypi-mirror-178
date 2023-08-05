# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kardiasclean']

package_data = \
{'': ['*']}

install_requires = \
['nltk==3.7', 'numpy==1.21.6', 'pandas==1.3.5', 'phonetics==1.0.5']

setup_kwargs = {
    'name': 'kardiasclean',
    'version': '0.1.1',
    'description': 'Medical Records Normalizer',
    'long_description': "# Kardiasclean\n\nClean, Normalize, and Tokenize medical records data.\n\n## Install\n\n```shell\npip install kardiasclean\n```\n\n## Usage\n\n```python\nimport kardiasclean\n\ndata['surgery'] = kardiasclean.split_string(data['surgery'])\ndata_map = kardiasclean.spread_column(data['surgery'])\n\ndata_map['surgery'] = kardiasclean.clean_accents(data_map['surgery'])\ndata_map['surgery'] = kardiasclean.clean_symbols(data_map['surgery'])\ndata_map['keywords'] = kardiasclean.clean_stopwords(data_map['surgery'])\ndata_map['token'] = kardiasclean.clean_tokenize(data_map['keywords'])s\n```\n\n## Development\n\n```shell\npoetry run pytest\n```\n\n## Changelog\n\n- 0.1.1: Small readme fixes.\n- 0.1.0: Initial Release.",
    'author': 'AlbertoV5',
    'author_email': '58243333+AlbertoV5@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/AlbertoV5/kardiasclean',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.6,<3.11',
}


setup(**setup_kwargs)
