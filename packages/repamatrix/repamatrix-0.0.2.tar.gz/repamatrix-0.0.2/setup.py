# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['repamatrix']

package_data = \
{'': ['*']}

install_requires = \
['blessed>=1.17.9,<2.0.0']

extras_require = \
{'colors': ['repacolors>=0.5.0,<0.6.0'],
 'image': ['pillow>=7.1.2,<10.0.0'],
 'webcam': ['opencv-contrib-python>=4.5.4,<5.0.0',
            'numpy>=1.21,<2.0',
            'mediapipe>=0.9.0,<0.10.0']}

entry_points = \
{'console_scripts': ['repamatrix = repamatrix:main',
                     'webcammatrix = repamatrix.webcam:main']}

setup_kwargs = {
    'name': 'repamatrix',
    'version': '0.0.2',
    'description': "cmatrix like terminal 'screen saver'",
    'long_description': '# `repamatrix`\n\n`cmatrix` like terminal *screen saver*\n\n![screenshot](./repamatrix.png)\n\n## Install\n\n```\n$ pip install repamatrix\n```\n\n## Running\n\n```\n$ repamatrix\n```\n\n### Webcam support\n\n```\n$ webcammatrix\n```\n\n',
    'author': 'Gyuri Horak',
    'author_email': 'dyuri@horak.hu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dyuri/repamatrix',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
