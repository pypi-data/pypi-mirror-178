import pathlib
from setuptools import setup, find_namespace_packages

long_description = pathlib.Path(__file__).parent.joinpath("README.md").read_text()

setup(
    name="pointevector-zip",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.0.3",
    author="Andrew Hoekstra",
    author_email="andrew@pointevector.com",
    url="https://github.com/Pointe-Vector/zip",
    packages=find_namespace_packages(),
    install_requires=[],
)
