from setuptools import setup, find_packages

setup(
    name="saft_data_mgmt",
    version="0.1.0",
    description="A package for managing financial data, specifically made for algorithmic traders.",
    long_description="This package helps with the management of data storage, etls, and warehousing for independent algorithmic traders. This includes storing historical price data for securities, strategy artifacts, portfolio performance information, and more.",
    long_description_content_type="text/markdown",
    author="Travis Swiger",
    author_email="tswiger@stoneagefinancialtechnology.com",
    url="https://github.com/S-A-F-T-Organization/DataManagement",
    packages=find_packages(),
    install_requires=[
        "SQLAlchemy>=1.4",
        "PyYAML"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    extras_require={
        "dev": ["twine>=4.0.2"],
    },
    python_requires='>=3.7',
)