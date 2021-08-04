from setuptools import find_packages, setup
from os import path

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, "README.md"), "r", encoding="utf-8") as f:
    long_description = f.read()

source_url = "https://github.com/samedamci/basedbinpy"

setup(
    name="basedbinpy",
    version="0.3.1",
    description="Simple python library for basedbin pastebin-like service.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="samedamci",
    author_email="samedamci@disroot.org",
    url=source_url,
    project_urls={
        "Source": source_url,
        "Tracker": f"{source_url}/issues",
    },
    install_requires=["requests", "bson==0.5.10"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    keywords="basedbin library api client",
    python_requires=">=3.6",
    packages=find_packages(include=["basedbinpy"]),
)
