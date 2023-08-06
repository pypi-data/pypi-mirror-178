from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A simple JSON string creator that takes whatever you have and transform it into an String'

# Setting up
setup(
    name='jsonwhatever',
    version=VERSION,
    author='dazjuancarlos',
    author_email='dazjuancarlos@gmail.com',
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    license='dazjuancarlos',
    keywords=['python','json','simple'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)