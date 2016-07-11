from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'ngram-tool',
    version = '0.0.1',
    description = 'A simple tool use for count ngram frequency.',
    long_description = long_description,
    url = 'https://github.com/dreamszl/ngram-tool',
    author = 'dreamszl',
    author_email = 'chenao3220@gmail.com',
    license = 'MIT',
    classifier = [
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Natural Language Processing,

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.7',
    ],
    keywords = 'ngram nlp',
    packages = find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires = [],
    extra_require = {
        'dev': [],
        'test': [],
    },
    package_data = {},
    data_files = [],
    entry_points = {
        'console_scripts': [],
    },
)
