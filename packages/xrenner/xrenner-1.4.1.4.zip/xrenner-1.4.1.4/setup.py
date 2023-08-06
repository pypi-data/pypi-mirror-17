from distutils.core import setup
from setuptools import find_packages

setup(
  name = 'xrenner',
  packages = find_packages(),
  version = '1.4.1.4',
  description = 'A configurable, language independent coreferencer and (non) named entity recognizer',
  author = 'Amir Zeldes',
  author_email = 'amir.zeldes@georgetown.edu',
  url = 'https://github.com/amir-zeldes/xrenner', 
  license='Apache License, Version 2.0',
  download_url = 'https://github.com/amir-zeldes/xrenner/tarball/1.4.1.4',
  keywords = ['NLP', 'coreference', 'NER', 'named entity'],
  classifiers = ['Programming Language :: Python',
'Programming Language :: Python :: 2',
'License :: OSI Approved :: Apache Software License',
'Operating System :: OS Independent'],
)