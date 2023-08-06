from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.3'
DESCRIPTION = 'Common libraries AISAC Bot'
LONG_DESCRIPTION = 'A package that contains the common libraries for the AISAC Bot'

# Setting up
setup(
    name="bot_common",
    version=VERSION,
    author="cla.fragomeli_92",
    author_email="<cla.fragomeli@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas', 'numpy'],
    keywords=['python', 'bot'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
