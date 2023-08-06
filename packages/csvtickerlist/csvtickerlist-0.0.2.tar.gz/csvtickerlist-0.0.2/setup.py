from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'Generate a CSV of all current tickers'
LONG_DESCRIPTION = 'A package that allows for the retrieval of a CSV file containing the full list of nearly all active ticker symbols.'

# Setting up
setup(
    name="",
    version=VERSION,
    author="Christian K.",
    author_email="<christiank1inquiries@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['selenium'],
    keywords=['python', 'stocks', 'tickers', 'algo-trading', 'finance'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)