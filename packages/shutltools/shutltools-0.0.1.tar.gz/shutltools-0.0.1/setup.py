from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='shutltools',
  version='0.0.1',
  description='Tools for SecretHeberg',
  long_description=open('README.md'),
  url='',  
  author='Noamane AIT ABDELLAH OUALI',
  author_email='noamane.fr@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='tools', 
  packages=find_packages(),
  install_requires=['requests'] 
)