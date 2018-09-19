from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='pycascades',
   version='1.0',
   description='A useful module',
   license="Internal PIK Project",
   long_description=long_description,
   author='Jonathan Krönke',
   author_email='kroenke@pik-potsdam.de',
   url="https://github.com/pik-copan/pycascades",
   packages=['modules'],
)
