# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['structured_data_validation',
 'structured_data_validation.conf',
 'structured_data_validation.database',
 'structured_data_validation.logging',
 'structured_data_validation.models',
 'structured_data_validation.scripts',
 'structured_data_validation.utils']

package_data = \
{'': ['*'],
 'structured_data_validation': ['.idea/*', '.idea/inspectionProfiles/*']}

install_requires = \
['coverage>=6.5.0,<7.0.0',
 'email-validator>=1.3.0,<2.0.0',
 'fastavro>=1.7.0,<2.0.0',
 'google-events>=0.2.0,<0.3.0',
 'hydra-colorlog>=1.2.0,<2.0.0',
 'hydra-core>=1.2.0,<2.0.0',
 'hydra-zen>=0.8.0,<0.9.0',
 'hypothesis>=6.56.4,<7.0.0',
 'importlib-metadata>=5.0.0,<6.0.0',
 'loguru>=0.6.0,<0.7.0',
 'pandas>=1.5.1,<2.0.0',
 'pyarrow>=9.0.0,<10.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'python-dotenv>=0.21.0,<0.22.0']

entry_points = \
{'console_scripts': ['validate = '
                     'structured_data_validation.scripts.validate_file:main']}

setup_kwargs = {
    'name': 'structured-data-validation',
    'version': '0.1.2',
    'description': 'Python package for the validation of AROS [semi]structured data using pydantic models.',
    'long_description': '# Structured data validation for AROS output files.\n\n[![Tests](https://github.com/jdiez/structured_data_validation/workflows/Tests/badge.svg)](https://github.com/jdiez/structured_data_validation/actions?workflow=Tests)\n[![PyPI](https://img.shields.io/pypi/v/structured_data_validation.svg)](https://pypi.org/project/structured_data_validation/)\n\nPython package for the validation of AROS [semi]structured data using pydantic models.\n\n[More coming soon]\n',
    'author': 'Javier Díez Pérez',
    'author_email': 'jdiezperezj@gmail.com',
    'maintainer': 'Javier Díez Pérez',
    'maintainer_email': 'jdiezperezj@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
