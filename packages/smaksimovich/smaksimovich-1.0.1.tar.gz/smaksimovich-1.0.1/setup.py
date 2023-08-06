from setuptools import setup

setup(
    name='smaksimovich',
    version='1.0.1',
    description='A personal library of random utility code',
    author='Sam Maksimovich',
    author_email='maksimovich.sam@gmail.com',
    packages=['smaksimovich'],
    install_requires=[
        'numpy',
        'torch',
    ]
)