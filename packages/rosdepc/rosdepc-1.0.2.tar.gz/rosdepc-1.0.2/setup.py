import os
from setuptools import setup

kwargs = {
    'name': 'rosdepc',
    'version': '1.0.2',
    'packages': ['rosdepc'],
    'package_dir': {'': 'src'},
    'install_requires': ['rosdep'],
    'author': '小鱼',
    'author_email': 'fishros@foxmail.com',
    'url': 'https://fishros.com',
    'keywords': ['ROS'],
    'entry_points': {
        'console_scripts': [
            'rosdepc = rosdepc.rosdepc:main',
        ]
    },
    'classifiers': [
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License'],
    'description': 'rosdep package manager abstraction tool for ROS',
    'long_description': 'Command-line tool for installing system '
                        'dependencies on a variety of platforms.',
    'license': 'BSD',
}
if 'SKIP_PYTHON_MODULES' in os.environ:
    kwargs['packages'] = []
    kwargs['package_dir'] = {}
if 'SKIP_PYTHON_SCRIPTS' in os.environ:
    kwargs['name'] += '_modules'
    kwargs['entry_points'] = {}

setup(**kwargs)
