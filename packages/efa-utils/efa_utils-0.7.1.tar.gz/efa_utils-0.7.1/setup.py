# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['efa_utils']

package_data = \
{'': ['*']}

install_requires = \
['factor-analyzer>=0.4.1,<0.5.0',
 'numpy>=1.23.5,<2.0.0',
 'pandas>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'efa-utils',
    'version': '0.7.1',
    'description': 'Custom utility functions for exploratory factor analysis with the factor_analyzer package.',
    'long_description': "# efa_utils\nCustom utility functions for exploratory factor analysis\n\n## Installation\nInstall with pip:\n```bash\npip install efa_utils\n```\n\n## Functions\n### efa_utils.reduce_multicoll\nFunction to reduce multicollinearity in a dataset (intended for EFA). Uses the determinant of the correlation matrix to determine if multicollinearity is present. If the determinant is below a threshold (0.00001 by default), the function will drop the variable with the highest VIF until the determinant is above the threshold. Requires statsmodels package.\n### efa_utils.kmo_check\nFunction to check the Kaiser-Meyer-Olkin measure of sampling adequacy (KMO) and Bartlett's test of sphericity for a dataset. Requires statsmodels package. Main use is to print a report of total KMO and item KMOs, but can also return the KMO values.\n\n### efa_utils.parallel_analysis\nFunction to perform parallel analysis to determine the number of factors to retain. Requires matplotlib.\n\n### efa_utils.iterative_efa\nFunction to perform iterative exploratory factor analysis. Runs EFA with an iterative process, eliminating variables with low communality, low main loadings or high cross loadings in a stepwise process. If parallel analysis option is to be used, requires matplotlib.\n\n### efa_utils.print_sorted_loadings\nPrint strongly loading variables for each factor. Will only print loadings above load_thresh for each factor.\n\n### efa_utils.rev_items_and_return\nTakes an EFA object and automatically reverse-codes (Likert-scale) items where necessary and adds the reverse-coded version to a new dataframe. Returns the new dataframe.\n\n### efa_utils.factor_int_reliability\nTakes a pandas dataframe and dictionary with name of factors as keys and list of variables as values. Prints results for the internal reliability for each factor. Requires reliability package.",
    'author': 'Marcel Wiechmann',
    'author_email': 'mail@mwiechmann.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
