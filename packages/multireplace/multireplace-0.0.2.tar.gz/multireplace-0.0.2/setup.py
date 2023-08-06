from setuptools import setup, find_packages

with open('README.md') as file:
    readme = file.read()

setup(
    name='multireplace',
    version='0.0.2',
    author='Oshten',
    description='Method for multi replace in strings',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/Oshten/multireplace',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)