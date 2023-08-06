# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wj_social_net_queries',
 'wj_social_net_queries.connectors',
 'wj_social_net_queries.controllers',
 'wj_social_net_queries.core',
 'wj_social_net_queries.utils',
 'wj_social_net_queries.utils.AWS',
 'wj_social_net_queries.utils.constants']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.24.45,<2.0.0',
 'certifi==2022.6.15',
 'charset-normalizer==2.1.0',
 'chromedriver-autoinstaller>=0.4.0,<0.5.0',
 'idna==3.3',
 'numpy==1.21.3',
 'pandas==1.3.2',
 'python-dateutil==2.8.2',
 'python-dotenv==0.20.0',
 'pytz==2022.1',
 'requests-oauthlib>=1.3.1,<2.0.0',
 'requests==2.28.1',
 'selenium>=4.4.3,<5.0.0',
 'six==1.16.0',
 'tweepy>=4.10.0,<5.0.0',
 'urllib3==1.26.11']

setup_kwargs = {
    'name': 'wj-social-net-queries',
    'version': '0.15.0',
    'description': "this library is responsible for comunicating with social network API's for data interaction with Whale and Jaguar products",
    'long_description': 'None',
    'author': 'w&j',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
