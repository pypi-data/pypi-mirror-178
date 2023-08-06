"""Library Metadata Information."""

from setuptools import find_packages
from setuptools import setup

description = ("rate limiting filter for python logging module.")

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="logging_rate_limiter",
    version="0.0.1",
    author="hitesh jha",
    author_email="hitesh4official@gmail.com",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jha-hitesh/logging-rate-limiter",
    packages=find_packages(
        exclude=(
            "tests"
        )
    ),
    license="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    python_requires=">=3.6",
)
