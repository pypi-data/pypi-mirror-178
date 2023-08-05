from setuptools import setup, find_packages
import codecs
import os


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

long_desc = "a data api only for test! "

def read_install_requires():
    reqs = [
            'pandas>=0.18.0',
            'requests>=2.0.0',
            'lxml>=3.8.0',
            'simplejson>=3.16.0',
            'msgpack>=0.5.6',
            'pyzmq>=16.0.0'
            ]
    return reqs


setup(
    name='mamamiya',
    version=read('mamamiya/VERSION.txt'),
    description='A utility for crawling historical and Real-time Quotes data of China stocks',
    long_description = long_desc,
    author='Jimmy Liu',
    author_email='jimmysoa@sina.cn',
    license='BSD',
    url='http://tushare.org',
    install_requires=read_install_requires(),
    keywords='Global Financial Data',
    classifiers=['Development Status :: 4 - Beta',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'License :: OSI Approved :: BSD License'],
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['*.csv', '*.txt']},
)