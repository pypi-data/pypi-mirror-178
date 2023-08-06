# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['psite_recommender']

package_data = \
{'': ['*']}

install_requires = \
['anndata>=0.8.0,<0.9.0',
 'implicit>=0.6.1,<0.7.0',
 'numpy>=1.23.4,<2.0.0',
 'pandas>=1.5.1,<2.0.0',
 'scanpy>=1.9.1,<2.0.0',
 'scvelo>=0.2.4,<0.3.0',
 'seaborn>=0.12.1,<0.13.0',
 'statsmodels>=0.13.2,<0.14.0']

setup_kwargs = {
    'name': 'psite-recommender',
    'version': '0.1.0',
    'description': 'RS for Proteomics',
    'long_description': '# Recommender_System_Proteomics\nScripts to run Recommender Systems on Proteomics data.\n\n## Downloading:\n  - click on the green "Code" button on the top right and Download ZIP, then unzip it  \n  or use  \n  - git clone https://github.com/ManuelGander/Recommender_System_Proteomics.git\n  \n## Running the scripts:\n  - The notebook "Full_script.ipynb" contains all the information needed to run the scripts\n',
    'author': 'Manuel Gander',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
