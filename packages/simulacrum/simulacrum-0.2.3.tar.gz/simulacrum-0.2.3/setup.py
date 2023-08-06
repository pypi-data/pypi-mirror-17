from setuptools import setup

setup(name = 'simulacrum',
      version = '0.2.3',
      description = 'Create Pandas DataFrames of simulated data with columns following statistical distributions or categorical datatypes',
      url = 'https://github.com/jbrambleDC/simulacrum',
      download_url = 'https://github.com/jbrambleDC/simulacrum/tarball/0.2.3',
      author = 'Jordan Bramble',
      author_email = 'jordanbramble@gmail.com',
      license = 'MIT',
      packages = ['simulacrum'],
      keywords = ['simulation', 'data', 'data science'],
      install_requires = ['pandas', 'faker'],
      zip_safe = False)
