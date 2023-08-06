from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.5'
DESCRIPTION = 'Date Time Persian'
LONG_DESCRIPTION = 'This library helps you to convert the Gregorian date to Iranian date and the Iranian date to Gregorian date.'

# Setting up
setup(
    name="DateTimePersian",
    version=VERSION,
    author="Erfan Mahigir (Sarzamin Danesh Pishro)",
    author_email="<info@Lssc.ir>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'Date', 'Persian', 'Time', 'Gregorian', 'Convert', 'Iranian'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
