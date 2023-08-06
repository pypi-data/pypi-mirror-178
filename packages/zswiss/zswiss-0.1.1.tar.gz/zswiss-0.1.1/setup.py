from setuptools import setup
from setuptools import find_packages

VERSION = '0.1.1'

with open("README.rst", "r") as f:
    long_description = f.read()

setup(name='zswiss',  # 包名
      version=VERSION,  # 版本号
      description='some tools, simple but useful',
      long_description=long_description,
      author='neilxzhang',
      author_email='legend_zhx@163.com',
      install_requires=[],
      license='MIT License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Topic :: Software Development :: Libraries'
      ],
      )
