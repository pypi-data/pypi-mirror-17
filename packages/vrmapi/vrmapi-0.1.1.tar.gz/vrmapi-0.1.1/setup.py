from setuptools import setup, find_packages

setup(
    name='vrmapi',
    packages=find_packages(),
    version='0.1.1',
    description='Victron api',
    install_requires=['requests'],
)
