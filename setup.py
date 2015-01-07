from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='BayesianBozo',
    version = '0.0.6',

    #packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    # A description of your project
    description='Bayesian statistical functions for Python',
    long_description='Bayesian statistical functions and algorithms Ive needed to build as I delve deeper into Bayesian Statistics',

    # The project's main homepage
    url='https://github.com/jcbozonier/BayesianBozo',

    # Author details
    author='Justin Bozonier',
    author_email='darkxanthos@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    # What does your project relate to?
    keywords='bayes statistics probability inferrence',

    install_requires = ['numpy'])