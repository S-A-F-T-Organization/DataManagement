"""This module contains the CLI tool for implementing a SAFT DB schema"""
from src.DataStorage.Utils.configurator import ConfigInfo

def generate_config():
    """
    Prompts the user for various inputs related to the database setup and returns a config dict.
    """
    config_info = ConfigInfo()

    # 1. SQL Dialect
    sql_dialect = input("What SQL dialect will you be using? (current support: sqlite, postgresql): ")
    config_info.db_dialect = sql_dialect.strip().lower()

    # 2. DB Path
    db_path = input("What is the path you would like to host this database at? (not including DB name): ")
    config_info.db_path = db_path.strip()

    # 3. DB Name
    db_name = input("3. What would you like to name this database? (should end in .db): ")
    config_info.db_name = db_name.strip()
    config_info.db_path = f"{config_info.db_path}/{config_info.db_name}"


    # 4. Market Data Schema
    enable_market_data = input("4. Would you like to implement our `market_data` schema? [Y/N]: ")
    if enable_market_data.lower() == 'y':
        config_info.market_data_flag = True


    if config_info.market_data_flag:
        store_prices_as_ints = input("Would you like to store historical security prices as integers? [Y/N]: ")
        if store_prices_as_ints.lower() == 'y':
            config_info.to_int_flag = True

        store_ohlcv = input("Would you like to store OHLCV data? [Y/N]: ")
        if store_ohlcv.lower() == 'y':
            config_info.ohlcv_flag = True

        store_quote_level = input("Would you like to store quote level data? [Y/N]: ")
        if store_quote_level.lower() == 'y':
            config_info.quotes_flag = True

        # Which securities to track
        securities_input = input("Of the following, which securities do you plan to track?" +
                                 "[Stocks, ETFs, Forex, Futures] (comma-separated): ")
        securities_list = [sec.strip() for sec in securities_input.split(',')]
        config_info.security_types = securities_list

        # Which seed data to insert
        seed_input = input("   Would you like to insert any of the seed data we offer?"
                           "[Security Types, Exchanges, Futures, Forex, Stocks, ETFs] (comma-separated): ")
        seed_data_list = [sd.strip() for sd in seed_input.split(',')]
        config_info.seed_data = seed_data_list

    # 5. Portfolio Data Schema
    enable_portfolio_data = input("Would you like to implement our `portfolio_data` schema? [Y/N]: ")
    if enable_portfolio_data.lower() == 'y':
        config_info.portfolio_data_flag = True

    return config_info
