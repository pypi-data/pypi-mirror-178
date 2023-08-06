from pathlib import Path

from setuptools import setup

# Globals and constants variables.
BASEDIR = Path(__file__).parent.resolve()

with open(BASEDIR.joinpath("README.md"), "r") as fp:
    LONG_DESCRIPTION = fp.read()

setup(
    name="pyroulette",
    version="0.0.5",
    description="A package for exploring roulette strategies.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Mathematical Michael",
    author_email="consistentbayes@gmail.com",
    url="https://git.clfx.cc/mm/roulette",
    packages=["pyroulette"],
    license="MIT",
    install_requires=["dataclasses; python_version<'3.7'"],
    python_requires=">=3.6, <4.0",
)
