"""Performs the setup for the saft_data_mgmt package."""

from setuptools import setup, find_packages

# Read the content of README.md file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="saft_data_mgmt",
    version="0.2.3",
    description="A package for managing financial data, specifically made for algorithmic traders.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Travis Swiger",
    author_email="tswiger@stoneagefinancialtechnology.com",
    url="https://github.com/S-A-F-T-Organization/DataManagement",
    entry_points={
        'console_scripts': [
            'setup-saft-db=saft_data_mgmt.setup_saft_db:main',
        ],
    },
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": ["**/SQLTables/**/*.sql"],
    },
    install_requires=["SQLAlchemy>=1.4", "PyYAML"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial",
        "Topic :: Database",
        "Development Status :: 3 - Alpha",
    ],
    extras_require={
        "dev": ["twine>=4.0.2", "build"],
    },
    python_requires=">=3.7",
)
