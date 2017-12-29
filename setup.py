import os
from setuptools import setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
        name='uvindx_info',
        version='1',
        packages=['uvindx_info'],
        install_requires=[],
        license='MIT License',
        description='Python library to look up timezone from lat / long offline',
        long_description='',
        url='https://github.com/pegler/pytzwhere',
        author='Andrew Sozonnyk',
        package_data={'uvindx_info': ['*.json']},
        author_email='matt@pegler.co',
        maintainer='Christoph Stich',
        maintainer_email='christoph@stich.xyz',
        classifiers=[
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 3',
            'Topic :: Software Development :: Localization',
        ],
)