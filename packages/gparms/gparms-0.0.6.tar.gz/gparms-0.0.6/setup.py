from setuptools import setup, find_packages
import os

VERSION = '0.0.6'
DESCRIPTION = 'Get URL Parameters'
LONG_DESCRIPTION = 'A tools that takes URLs from stdin and outputs URLs with parameters.'

# Setting up
setup(
    name="gparms",
    version=VERSION,
    author="Shelled",
    description=DESCRIPTION,
    packages=find_packages(),
    keywords=['python', 'bug bounty', 'pentesting', 'url'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={
        'console_scripts': [
            'gparms = gparms.gparms:main'
        ]
    }
)
