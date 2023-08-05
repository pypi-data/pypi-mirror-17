from setuptools import setup
from os import path

readme = path.join(path.abspath(path.dirname(__file__)), "README.md")

with open(readme, "r") as file:
    long_desc = file.read()

setup(
    name='gito',
    version='2.0',
    description='Tool to view list of Git TODO`s and sync with wunderlist',
    long_description=long_desc,
    author='raghu',
    author_email='raghu12133@gmail.com',
    url='https://github.com/raghu12133/gito',
    install_requires=[
        'termcolor',
        'requests',
        'pyyaml',
        'pathspec'
    ],
    packages = ['src'],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
    ],
    entry_points = {
        'console_scripts': [
            'gito=src.main:execute'
        ]
    }
)
