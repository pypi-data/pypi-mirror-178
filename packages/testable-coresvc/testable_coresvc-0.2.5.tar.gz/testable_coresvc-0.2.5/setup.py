from setuptools import setup, find_packages

VERSION = "0.2.5"
DESCRIPTION = 'Core Testable Service Modules'
LONG_DESCRIPTION = 'Core service modules that provide access to shared functionality across Testable services.'

# Setting up
setup(
    name="testable_coresvc",
    version=VERSION,
    author="Ryan de Marigny",
    author_email="testableproject@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["pydantic>=1.10.2", "typing_extensions>=4.4.0", "fastapi>=0.87.0", "pymongo>=4.3.3"],

    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
