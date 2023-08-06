from setuptools import setup

requires = ["requests"]

setup(
    name="",
    version="0.0.3",
    url="https://github.com/ishtos/pyjoepegs",
    description="client library for joepegs api",
    author="ishtos",
    license="APACHE LICENSE, VERSION 2.0",
    packages=["pyjoepegs"],
    install_requires=requires,
    classifiers=["Programming Language :: Python"],
    keywords=["pyjoepegs", "joepegs"],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
