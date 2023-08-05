from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Education",
    "Operating System :: Microsoft :: Windows :: Windows 11",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3"
]

setup(
    name="randrandom",
    version="0.0.1",
    description="Improvment on the random libary.",
    long_description=open("README.txt").read() + "\n\n" + open("CHANGELOG.txt").read(),
    url="",
    author="Abubakr",
    author_email="abubakr.sultan14@gmail.com",
    license="MIT",
    classifiers=classifiers,
    keywords="random",
    packages=find_packages(),
    install_requires=[""]
)