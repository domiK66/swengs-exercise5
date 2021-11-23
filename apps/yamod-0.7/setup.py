from setuptools import setup, find_packages
import os.path

setup(
    name='yamod',
    version="0.7",
    author='FH JOANNEUM Gesellschaft mbH',
    author_email='karl.kreiner@fh-joanneum.at',
    packages=find_packages(),
    include_package_data=True,
    scripts=[],
    url='https://www.fh-joanneum.at/',
    license='LICENSE.txt',
    description='Yet another movie database - a django app for movie data management for educational purposes',
    long_description=open('README.md').read(),
    install_requires=[
        "django==3.2.8"
    ],
)

