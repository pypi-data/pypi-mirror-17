from setuptools import setup, find_packages
import os


ROOT = os.path.abspath(os.path.dirname(__file__))
VERSION = '1.1'

def get_requirements(filename):
    return open(os.path.join(ROOT, filename)).read().splitlines()

setup(
  name='ndic',
  # packages = ['ndic'],
  packages=find_packages(),
  include_package_data=True,
  # py_modules=['ndic'],
  install_requires=get_requirements('requirements.txt'),
  tests_require=get_requirements('test-requirements.txt'),
  version=VERSION,
  description='Python module for NAVER English-Korean and Korean-English dictionaries',
  long_description=open(os.path.join(ROOT, 'README.md')).read(),
  author='jupiny',
  author_email='tmdghks584@gmail.com',
  url='https://github.com/jupiny/ndic',
  download_url='https://github.com/jupiny/ndic/tarball/1.0',
  dependency_links = ['https://github.com/jupiny/ndic/tarball/1.0'],
  # keywords = ['dictionary', 'translate', 'English', 'Korean', 'Naver'],
  classifiers=[],
  test_suite='nose.collector',
  entry_points='''
    [console_scripts]
    ndic=ndic.scripts.search:search
  ''',
)
