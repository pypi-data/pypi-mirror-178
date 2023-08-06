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
    version="0.0.2",
    description="Improvment on the random libary.",
    long_description="This is a simple random libary that adds on to the random libary. \n Functions: \n - randinteger \n - randfloat \n - randbytes \n -rand \n - randeven \n - randodd \n -randitem \n -randletter \n - randduplicate \n\n Change Log: \n === \n\n 0.0.1 (2022-11-23) \n === \n - Release \n === \n\n 0.0.2 (2022-11-24) \n === \n - Added more functions \n - Fixed randeven and randodd",
    url="",
    author="Abubakr",
    author_email="abubakr.sultan14@gmail.com",
    license="MIT",
    classifiers=classifiers,
    keywords="random",
    packages=find_packages(),
    install_requires=[""]
)