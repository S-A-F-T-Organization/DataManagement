# DataManagement
## Table of Contents

## Overview

This is our core repository for managing financial data, designed to support algorithmic trading strategies. It provides tools for:

*   **Data Storage:** Efficient storage of historical market data and portfolio data.
*   **ETL Processes:** Extracting, transforming, and loading data from various sources (brokerages, APIs, etc.) into a usable format.
*   **Data Warehousing:** Structuring portfolio data for analysis and reporting.
*   **Database Agnostic Design:** Ensuring compatibility with different database engines and designs.
*   **CLI Tool:** A command-line interface for setting up and configuring the database.

## Integrations

### Database Integrations

*   SQLite (currently supported)
*   PostgreSQL (future support)

### Brokerage and Datasource Integrations

*   Interactive Brokers (IBKR)
*   yfinance (future support)

## Installation Instructions

1.  **Prerequisites:**
    *   Python 3.7 or higher
    *   pip (Python package installer)
    *   SQLite3 or PostgreSQL (future support)

2.  **Install the package using pip:**

    ```bash
    pip install saft_data_mgmt
    ```
## CLI Tool
This is a CLI tool that allows for easy setup of our normalized database. By answering a few questions in the command line, a database is setup according to your needs.
### Usage Instructions
1.  **Run the CLI Tool:**

    After installing the package, you can use the command-line tool to set up your database. Open your terminal and run:

    ```bash
    setup-saft-db
    ```

    or

    ```bash
    python -m saft_data_mgmt.setup_saft_db
    ```

2.  **Follow the Prompts:**

    The CLI tool will guide you through a series of questions to configure your database. These questions include:

    *   Database dialect (e.g., SQLite)
    *   Database path
    *   Database name
    *   Whether to implement market data and portfolio data schemas
    *   Additional options for market data (e.g., storing historical prices as integers)

3.  **Configure Database:**

    Answer the questions according to your needs. The tool will then set up the database with the specified configurations.

    **Note:** There is a known error with the undo functionality, so using `CTRL + Z` will not undo an answer and go to the previous question

### Example Usage

Here's an example of how to use the CLI tool to set up a SQLite database:

```bash
setup-saft-db
```
You will then be prompted with the following questions:
```bash
1. What SQL dialect will you be using? (current support: sqlite): sqlite
2. What is the path you would like to host this database at? (not including DB name): /path/to/your/db
3. What would you like to name this database? (should end in .db): saft.db
4. Would you like to implement our `market_data` schema? [Y/N]: Y
5. Would you like to implement our `portfolio_data` schema? [Y/N]: N
6. Would you like to store historical security prices as integers? [Y/N]: Y
7. Of the following, which securities do you plan to track? [Stocks, ETFs, Forex, Futures, All] (comma-separated): Stocks, ETFs
```

## Contribution Guidelines

This project is a work in progress, but we love your input! We want to make contributing to SAFT Data Management as easy possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

### Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue a pull request

### Pull Request Process

1. Update the README.md with details of changes to the interface, if applicable.
2. Update the version numbers in any examples files and the README.md to the new version that this Pull Request would represent.
3. The PR will be merged once you have the sign-off of two other developers.

### Any contributions you make will be under the Apache 2.0 Software License

In short, when you submit code changes, your submissions are understood to be under the same [Apache 2.0 License](http://choosealicense.com/licenses/apache-2.0/) that covers the project. Feel free to contact the maintainers if that's a concern.

### Report bugs using GitHub's [issue tracker](https://github.com/S-A-F-T-Organization/DataManagement/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/S-A-F-T-Organization/DataManagement/issues/new).

### Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can.
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

### Code Style and Standards

#### Python Style Guide

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some modifications:

- Line length limit: 115 characters
- Use spaces for indentation (4 spaces)
- Use docstrings for all public modules, functions, classes, and methods
- Use type hints for function arguments and return values

Example:
```python
def calculate_return(price: float, cost_basis: float) -> float:
    """Calculate the return on investment.

    Args:
        price (float): Current price of the security
        cost_basis (float): Original purchase price

    Returns:
        float: The percentage return on investment
    """
    return (price - cost_basis) / cost_basis * 100
```

#### SQL Style Guide

- Use UPPERCASE for SQL keywords
- Use PascalCase for table names
- Use snake_case for column names
- Include appropriate comments for complex queries
- Each column on a new line for readability

Example:
```sql
CREATE TABLE IF NOT EXISTS security_prices (
    security_id INTEGER,
    price_timestamp INTEGER,
    close_price INTEGER,
    PRIMARY KEY (security_id, price_timestamp),
    FOREIGN KEY (security_id) 
        REFERENCES securities_info(security_id)
);
```

### Testing Guidelines

1. **Unit Tests Required:**
   - All new features must include unit tests
   - Bug fixes must include tests that would have caught the bug
   - Use of unittest library

2. **Running Tests:**
```bash
# Run all tests
python -m unittest
```

3. **Test Structure:**
   - Use descriptive test names
   - Follow the Arrange-Act-Assert pattern
   - Mock external dependencies

### Documentation Requirements

1. **Code Documentation:**
   - All public APIs must have docstrings
   - Include type hints
   - Document exceptions that may be raised

2. **Project Documentation:**
   - Update README.md for interface changes
   - Maintain documentation in /docs directory
   - Include examples for new features

### Version Control Guidelines

1. **Branching Strategy:**
   - `main`: stable, production-ready code
   - `dev`: integration branch for features
   - `NameDev`: Replace with either your name or username as your personal dev branch

2. **Commit Messages:**
   - Use present tense
   - First line is summary (50 chars or less)
   - Reference issues and pull requests

Example:
```
Add historical price integer conversion

- Implement price to integer conversion utility
- Add tests for conversion edge cases
- Update documentation with new feature

Fixes #123
```

### Release Process

1. Version numbers follow [SemVer](http://semver.org/)
2. Create a release branch from dev
3. Update version numbers
4. Update CHANGELOG.md
5. Create pull request to main
6. Tag the release
7. Deploy to PyPI

## Project Structure
```
DataManagement/ 
├── LICENSE
├── MANIFEST.in
├── README.md
├── setup.py
├── saft_data_mgmt/
│ ├── init.py
│ ├── main.py # Enables python -m saft_data_mgmt
│ ├── setup_saft_db.py # Main CLI module
│ ├── Utils/
│ │ ├── init.py
│ │ ├── cli_checks.py
│ │ ├── cli_tool.py
│ │ ├── config_info.py
│ │ ├── db_from_config.py
│ │ ├── db_strategies.py
│ │ └── helpers.py
│ ├── SQLTables/
│ │ ├── Core/
│ │ ├── HistoricalPrices/
│ │ ├── PortfolioDB/
│ │ └── PortfolioWarehouse/ 
├── tests/
```
