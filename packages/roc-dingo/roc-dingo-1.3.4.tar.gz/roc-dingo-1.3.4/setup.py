# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['roc',
 'roc.dingo',
 'roc.dingo.models',
 'roc.dingo.models.versions',
 'roc.dingo.tasks',
 'roc.dingo.templates',
 'roc.dingo.tests',
 'roc.dingo.tests.test-1-tasks',
 'roc.dingo.tests.test-2-commands']

package_data = \
{'': ['*'],
 'roc.dingo.models.versions': ['SQL/*'],
 'roc.dingo.tests': ['data-tasks/*']}

install_requires = \
['SQLAlchemy>=1.3,<2.0',
 'alembic>=1.4,<2.0',
 'numpy!=1.19.5',
 'pandas>=1.1.3',
 'poppy-core>=0.9.4',
 'poppy-pop>=0.7.5',
 'psycopg2>=2.8.4,<3.0.0',
 'roc-idb>=1.0,<2.0',
 'roc-rpl>=1.0,<2.0',
 'spacepy>=0.4.1,<0.5.0',
 'spice_manager>=1.1.0,<2.0.0',
 'xmltodict>=0.13,<0.14']

setup_kwargs = {
    'name': 'roc-dingo',
    'version': '1.3.4',
    'description': 'Data INgestOr (DINGO) plugin is used to ingest data into the ROC pipeline database',
    'long_description': 'DINGO PLUGIN README\n===================\n\n[![pipeline status](https://gitlab.obspm.fr/ROC/Pipelines/Plugins/DINGO/badges/develop/pipeline.svg)](https://gitlab.obspm.fr/ROC/Pipelines/Plugins/DINGO/pipelines)\n[![coverage report](https://gitlab.obspm.fr/ROC/Pipelines/Plugins/DINGO/badges/develop/coverage.svg)](https://roc.pages.obspm.fr/Pipelines/Plugins/DINGO/pytest_coverage_html/)\n[![tests status](https://roc.pages.obspm.fr/Pipelines/Plugins/DINGO/pie.svg)](https://roc.pages.obspm.fr/Pipelines/Plugins/DINGO/report.html)\n\nThis directory contains the source files of the Data INGestOr (DINGO), a plugin of the ROC pipeline used to ingest data into the ROC database.\nDINGO is developed with and run under the POPPY framework.\n',
    'author': 'Florence Henry',
    'author_email': 'florence.henry@obspm.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.obspm.fr/ROC/Pipelines/Plugins/DINGO',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
