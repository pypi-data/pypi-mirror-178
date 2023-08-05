from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "readme.md"), encoding="utf-8") as fh:
    long_descriptionn = "\n" + fh.read()

VERSION = '0.0.6'
DESCRIPTION = 'Create a DAPP for your organisation and Manage all your Organisational Activities.'
LONG_DESCRIPTION = 'Create a DAPP for your organisation. \n Create Wallets for Employees in your Organistion. \n Manage their Leaves, Attendence, Proof of Learnings and Proof of Experiences.'

# Setting up
setup(
    name="pluaris-sdk",
    version=VERSION,
    author="Chethan Pasupuleti",
    author_email="<chethanpss24@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_descriptionn,
    packages=find_packages(),
    install_requires=['requests' ],
    keywords=['python', 'pluaris', 'algorand', 'sdk','smart contract'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)