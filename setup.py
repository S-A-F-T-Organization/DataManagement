from setuptools import setup, find_packages

setup(
    name="saft_data_mgmt",
    version="0.1.0",
    description="A package for managing financial data, specifically made for algorithmic traders",
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
    python_requires='>=3.7',
)