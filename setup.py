from setuptools import find_packages, setup

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="basedbinpy",
    packages=find_packages(include=["basedbinpy"]),
    version="0.2",
    description="Simple python library for basedbin pastebin-like service",
    author="samedamci",
    license="ISC",
    install_requires=requirements
)
