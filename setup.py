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
        description='uvindx.info website',
        long_description='',
        url='https://github.com/sozonnyk/uvindx.info',
        author='Andrew Sozonnyk',
        package_data={'uvindx_info': ['*.json']},
        author_email='andrew@sozonnyk.com',
        maintainer='Andrew Sozonnyk',
        maintainer_email='andrew@sozonnyk.com',
        classifiers=[
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3'
        ],
)