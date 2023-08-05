from setuptools import setup, find_packages


setup(
    name = 'tesoro_client',
    version = '0.1.0',
    packages = find_packages(exclude=['tests']),
    install_requires = ['requests>=2.6', 'responses', 'nose'],
    url = 'https://github.com/octoenergy/tesoro-lib',
)
