# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['satellite_weather_downloader',
 'satellite_weather_downloader.celery_app',
 'satellite_weather_downloader.utils']

package_data = \
{'': ['*']}

install_requires = \
['MetPy>=1.3.1,<2.0.0',
 'SQLAlchemy>=1.4.41,<2.0.0',
 'cdsapi>=0.5.1,<0.6.0',
 'netCDF4>=1.6.1,<2.0.0',
 'numpy>=1.23.3,<2.0.0',
 'pandas>=1.5.0,<2.0.0',
 'psycopg2-binary>=2.9.4,<3.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'satellite-weather-downloader',
    'version': '1.2.0',
    'description': 'The routines available in this package are designed to capture and process satellite images',
    'long_description': '<!-- satellite_weather_downloader -->\n',
    'author': 'Flavio Codeco Coelho',
    'author_email': 'fccoelho@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/osl-incubator/satellite-weather-downloader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
