from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='klld',
    version='5.0.1',
    description='klld@email.com',
    author= 'klld',
    url = '',
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=['klldv5', 'fortnte', 'fortnite bot'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=['klldv5'],
    package_dir={'':'src'},
    install_requires = [
          'crayons',
          'PirxcyPinger',
          'fortnitepy'
          'BenBotAsync',
          'FortniteAPIAsync',
          'sanic',
          'aiohttp',
          'uvloop',
          'requests'  
    ]
)
