import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='johansen',
      version='0.0.4',
      description='Python implementation of the Johansen test for cointegration',
      author='Isaiah Yoo',
      author_email='yoo.isaiah@gmail.com',
      maintainer='Isaiah Yoo',
      maintainer_email='yoo.isaiah@gmail.com',
      license='MIT License',
      url='https://github.com/iisayoo/johansen',
      long_description=read('README'),
      packages=find_packages(),
      install_requires=[
          'scipy>=0.18.0',
          'statsmodels>=0.6.1',
          'numpy>=1.11.1',
          'pandas>=0.18.1',
      ],
      include_package_data=True,
)
