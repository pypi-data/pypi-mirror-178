# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fs', 'fs.dropboxfs']

package_data = \
{'': ['*']}

install_requires = \
['dropbox>=11.36.0', 'fs>=2.0.10']

entry_points = \
{'fs.opener': ['dropbox = fs.dropboxfs.opener:DropboxOpener']}

setup_kwargs = {
    'name': 'fs.dropboxfs',
    'version': '0.3.0',
    'description': 'Pyfilesystem2 implementation for Dropbox',
    'long_description': "# fs.dropboxfs\n\nImplementation of pyfilesystem2 file system using Dropbox\n\n![image](https://github.com/rkhwaja/fs.dropboxfs/workflows/ci/badge.svg) [![PyPI version](https://badge.fury.io/py/fs.dropboxfs.svg)](https://badge.fury.io/py/fs.dropboxfs)\n\n# Usage\n\n``` python\nfrom fs import open_fs\nfrom fs.dropboxfs import DropboxFS\n\ndropboxFS = DropboxFS(\n  accessToken=<your access token>,\n  refreshToken=<your refresh token>)\n\ndropboxFS2 = open_fs('dropbox:///somedirectory?access_token=your_access_token&refresh_token=your_refresh_token')\n\n# dropboxFS and dropboxFS2 are now a standard pyfilesystem2 file system\n```\n",
    'author': 'Rehan Khwaja',
    'author_email': 'rehan@khwaja.name',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rkhwaja/fs.dropboxfs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
