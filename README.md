# DataManagement
## Table of Contents

## Overview
This is our core repository for managing data, and will be open source. As of now, the key packages that we are developing/will develop are the DataStorage and ETLs packages.The data storage will be centered around efficient storage of historical market data, and datawarehousing of portfolio data for analysis. Other possible modules will include an automated feature store and other key aspects of model development. The ETLs package will be focused on getting data from a source, whether it be the users portfolio, historical data from a brokerage, data from yfinance, etc., transforming that data into a usable/space optimized form, and loading it into the user's database. This should be database engine agnostic and database design agnostic. This will mean the user should be able to access whatever data they need through the defined classes/methods.

## Integrations
### Database Integrations

### Brokerage and Datasource Integrations

## Project Structure
```
DataManagement/
├── config/
│   ├── database_config_template.yml # Users can specify different setups, i.e. equities only, futures only,
│   └── ...
├── core/
│   ├── __init__.py
│   ├── database/
│   │   ├── erd_market_data.png # ERDs of the databases
│   │   ├── erd_portfolio.png
│   │   ├── create_market_data_tables.sql # Defined tables for the databases 
│   │   ├── create_portfolio_tables.sql
│   │   ├── seed_data/
│   │   │   ├── 01_insert_security_types.sql # Important seed data
│   │   │   └── 02_insert_exchange_info.sql
│   │   ├── db_initializer.py # Creates the databases according to users preferences
│   │   └── ...
│   ├── etl/ # Has all of the the common etl functions/objects for historical data and portfolio data
│   │   ├── market_data_etl.py
│   │   ├── portfolio_etl.py
│   │   └── ...
│   └── ...
├── tests/ # testing suite
│   ├── test_broker_integrations/
│   ├── test_etl/
│   ├── test_db_initializer.py
│   └── ...
├── setup.py
└── README.md
```
## Database Package

## ETLs Package

## Contributing