from setuptools import setup, find_packages

__author__ = 'Michiaki Ariga'

setup(
  name='tabula-py',
  version='0.2.0',
  description='Simple wrapper for tabula, read tables from PDF into DataFrame',
  author=__author__,
  author_email='chezou@gmail.com',
  url='https://github.com/chezou/tabula-py',
  classifiers=[
    'Development Status :: 4 - Beta',
    'Topic :: Text Processing :: General',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3 :: Only',
  ],
  include_package_data=True,
  packages=find_packages(),
  license='MIT License',
  keywords=['data frame', 'pdf', 'table'],
  install_requires=[
    'pandas',
  ],
)
