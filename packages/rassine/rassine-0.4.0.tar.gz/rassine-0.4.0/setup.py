# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rassine',
 'rassine.imports',
 'rassine.lib',
 'rassine.matching',
 'rassine.rassine',
 'rassine.stacking',
 'rassine.tools']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=5.0.4,<6.0.0',
 'configpile[parsy,rich]>=10.1.0,<11.0.0',
 'filelock>=3.6.0,<4.0.0',
 'matplotlib>=3.3.4,<4.0.0',
 'nptyping>=1.4.4,<2.0.0',
 'numpy>=1.23.0,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'parsy>=1.4.0,<2.0.0',
 'recursive-diff>=1.1.0,<2.0.0',
 'rich>=11.2.0,<12.0.0',
 'scipy>=1.8.1,<2.0.0',
 'tybles>=0.3.2,<0.4.0',
 'typeguard>=2.13.3,<3.0.0',
 'typing-extensions>=4.1.1,<5.0.0']

extras_require = \
{'docs': ['furo==2022.09.29',
          'myst-nb>=0.17.1,<0.18.0',
          'sphinx>=5.3.0,<6.0.0',
          'sphinx-argparse>=0.4.0,<0.5.0',
          'sphinx-autodoc-typehints>=1.19.5,<2.0.0',
          'sphinxcontrib-bibtex>=2.5.0,<3.0.0',
          'sphinxcontrib-programoutput>=0.17,<0.18']}

entry_points = \
{'console_scripts': ['compare_normalized_output = '
                     'rassine.tools.compare_normalized_output:cli',
                     'enumerate_table_column_unique_values = '
                     'rassine.tools.enumerate_table_column_unique_values:cli',
                     'enumerate_table_rows = '
                     'rassine.tools.enumerate_table_rows:cli',
                     'matching_anchors_filter = '
                     'rassine.matching.matching_anchors_filter:cli',
                     'matching_anchors_scan = '
                     'rassine.matching.matching_anchors_scan:cli',
                     'matching_diff = rassine.matching.matching_diff:cli',
                     'pickle_compare = rassine.tools.pickle_compare:cli',
                     'preprocess_import = '
                     'rassine.imports.preprocess_import:cli',
                     'preprocess_table = rassine.imports.preprocess_table:cli',
                     'rassine = rassine.rassine.rassine:cli',
                     'reinterpolate = rassine.imports.reinterpolate:cli',
                     'reorder_csv = rassine.tools.reorder_csv:cli',
                     'sort_csv = rassine.tools.sort_csv:cli',
                     'stacking_create_groups = '
                     'rassine.stacking.stacking_create_groups:cli',
                     'stacking_master_spectrum = '
                     'rassine.stacking.stacking_master_spectrum:cli',
                     'stacking_stack = rassine.stacking.stacking_stack:cli']}

setup_kwargs = {
    'name': 'rassine',
    'version': '0.4.0',
    'description': 'RASSINE astronomy tool',
    'long_description': '# RASSINE\n![RASSINE logo](docs/source/_static/logo.png)\n\n[See the RASSINE website.](https://pegasilab.github.io/rassine/)',
    'author': 'Michael Cretignier',
    'author_email': 'michael.cretignier@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pegasilab/rassine.git',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
