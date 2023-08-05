# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['volttron', 'volttron.services.web']

package_data = \
{'': ['*'],
 'volttron.services.web': ['static/*',
                           'static/js/*',
                           'static/specs/*',
                           'templates/*']}

install_requires = \
['PyJWT==1.7.1',
 'argon2-cffi>=21.3.0,<22.0.0',
 'jinja2-cli>=0.7.0',
 'passlib>=1.7.4,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'treelib>=1.6.1',
 'volttron>=10.0.1a43,<11.0',
 'werkzeug>=2.1.2',
 'ws4py>=0.5.1']

setup_kwargs = {
    'name': 'volttron-lib-web',
    'version': '0.1.1a1',
    'description': '',
    'long_description': 'This package provides web services for the VOLTTRON™ platform.\nThis includes a RESTful API for interacting with the platform\nand utility pages for administration and certificate management.\nThis library cannot be installed as a VOLTTRON agent is.\nRather, it must be installed as a python package.\n\n[![Run Pytests](https://github.com/eclipse-volttron/volttron-lib-web/actions/workflows/run-test.yml/badge.svg)](https://github.com/eclipse-volttron/volttron-lib-web/actions/workflows/run-test.yml)\n[![pypi version](https://img.shields.io/pypi/v/volttron.svg)](https://pypi.org/project/volttron-core/)\n\n## Requirements\n* python >=3.8\n* volttron >= 10.0\n\n## Installation with Web\nThis library can be installed using pip:\n\n```bash\n> pip install volttron-lib-web\n```\n\nOnce the library is installed, VOLTTRON will not be able to start until the\nweb service is configured. Configurations for services, including this, reside\nin a service_config.yml file in the VOLTTRON_HOME directory\n(by default ~/.volttron/service_config.yml).\nIf this file does not already exist, create it. To configure the web service,\ninclude the following:\n\n```yaml\nvolttron.services.web:\n  enabled: true\n  kwargs:\n    bind_web_address: http://127.0.0.156:5467\n    web_secret_key: some_string # If not using SSL.\n    web_ssl_cert: /path/to/certificate # Path to the SSL certificate to be used by the web service. \n    web_ssl_key: /path/to/key # Path to the SSL secret key file used by web service.\n```\n\nIf using SSL, both web_ssl_certificate and web_ssl_key are required\nand web_secret_key should not be included. If SSL is not desired,\nprovide a web_secret_key instead and remove the lines for the web_ssl_cert\nand web_ssl_key.\n\nFull VOLTTRON documentation is available at [VOLTTRON Readthedocs](https://volttron.readthedocs.io)\n\n## Development\n\nPlease see the following for contributing guidelines [contributing](https://github.com/eclipse-volttron/volttron-core/blob/develop/CONTRIBUTING.md).\n\nPlease see the following helpful guide about [developing modular VOLTTRON agents](https://github.com/eclipse-volttron/volttron-core/blob/develop/DEVELOPING_ON_MODULAR.md)\n\n# Disclaimer Notice\n\nThis material was prepared as an account of work sponsored by an agency of the\nUnited States Government.  Neither the United States Government nor the United\nStates Department of Energy, nor Battelle, nor any of their employees, nor any\njurisdiction or organization that has cooperated in the development of these\nmaterials, makes any warranty, express or implied, or assumes any legal\nliability or responsibility for the accuracy, completeness, or usefulness or any\ninformation, apparatus, product, software, or process disclosed, or represents\nthat its use would not infringe privately owned rights.\n\nReference herein to any specific commercial product, process, or service by\ntrade name, trademark, manufacturer, or otherwise does not necessarily\nconstitute or imply its endorsement, recommendation, or favoring by the United\nStates Government or any agency thereof, or Battelle Memorial Institute. The\nviews and opinions of authors expressed herein do not necessarily state or\nreflect those of the United States Government or any agency thereof.',
    'author': 'Craig Allwardt',
    'author_email': 'craig.allwardt@pnnl.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://volttron.readthedocs.io',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
