from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='pysqlizer',
   version='1.0',
   description='A module that can be used to convert a CSV file into a SQL file',
   author='Sabeur Lafi',
   author_email='lafi.saber@gmail.com',
   url="https://github.com/slafi",
   license="MIT",
   long_description=long_description,
   packages=['pysqlizer'],
)