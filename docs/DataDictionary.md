# Data Dictionary

Below is the data dictionary for the tables based on the provided SQL definitions.

## Table of Contents

- [Core Tables](#core-tables)
- [Historical Prices](#historical-prices)
  - [OHLCV Tables](#ohlcv-tables)
  - [Options Tables](#options-tables)
  - [Consolidated Quotes](#consolidated-quotes)
  - [MBP Full](#mbp-full)
- [Securities Metadata](#securities-metadata)
  - [Cash Table](#cash-table)
  - [Currencies Table](#currencies-table)
  - [Earnings History](#earnings-history)
  - [Equities Snapshots](#equities-snapshots)
  - [ETF Table](#etf-table)
  - [Fundamentals Snapshots](#fundamentals-snapshots)
  - [Futures Table](#futures-table)
  - [Industry Info](#industry-info)
  - [Issuers Table](#issuers-table)
  - [Mutual Fund Snapshots](#mutual-fund-snapshots)
  - [Sector Info](#sector-info)
  - [Stock Splits Table](#stock-splits-table)
  - [Stock Table](#stock-table)
  - [Underlying Assets Table](#underlying-assets-table)
- [Portfolio Database](#portfolio-database)
  - [Account Info](#account-info)
  - [All Orders](#all-orders)
  - [Cancelled Orders](#cancelled-orders)
  - [Conditional Orders](#conditional-orders)
  - [Executed Orders](#executed-orders)
  - [Inference Steps](#inference-steps)
  - [Inference Times](#inference-times)
  - [Inferences](#inferences)
  - [Model Libraries](#model-libraries)
  - [Model Types](#model-types)
  - [Models](#models)
  - [Order Actions](#order-actions)
  - [Order Types](#order-types)
  - [Sessions](#sessions)
  - [Strategies](#strategies)
  - [Strategy Modules](#strategy-modules)
  - [Transaction Types](#transaction-types)
  - [Transactions](#transactions)

## Core Tables

| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| security_id           | INTEGER   | Unique identifier for each security                                       | securities_info      |
| security_name         | TEXT      | Name of the security                                                      | securities_info      |
| security_symbol       | TEXT      | Trading symbol of the security                                            | securities_info      |
| exchange_id           | INTEGER   | Unique identifier for each exchange                                       | security_exchange    |
| exchange_name         | TEXT      | Name of the exchange                                                      | security_exchange    |
| exchange_country      | TEXT      | Country where the exchange is located                                     | security_exchange    |
| security_type_id      | INTEGER   | Unique identifier for each security type                                  | security_types       |
| security_type_name    | TEXT      | Name of the security type                                                 | security_types       |
| to_int                | INTEGER   | Number of factors of 10 to get a security's price to an integer + 2       | securities_info      |

## Historical Prices
These are all of the tables we currently offer for tracking historical prices across various securities and in different schemas. This inlcudes our OHLCV security and options prices, along with our mbp and trade quotes schemas. The primary differences between the mbp and trades quotes schemas is that the trade schema is perfect when only dealing with top of book data (the best bids and asks) and tracking every trade made.
### OHLCV Tables

| Field Name            | Data Type | Definition                                                                 | Table                          |
|-----------------------|-----------|---------------------------------------------------------------------------|--------------------------------|
| ohlcv_id              | INTEGER   | Unique identifier for each OHLCV record                                   | security_prices_ohlcv_int      |
| symbol_id             | INTEGER   | Unique identifier for the security                                        | security_prices_ohlcv_int      |
| timestamp_utc_ms      | INTEGER   | Timestamp in UTC milliseconds                                             | security_prices_ohlcv_int      |
| open_price            | INTEGER/REAL   | Opening price of the security (scaled by `to_int`)                        | security_prices_ohlcv_int      |
| high_price            | INTEGER/REAL  | Highest price of the security (scaled by `to_int`)                        | security_prices_ohlcv_int      |
| low_price             | INTEGER/REAL   | Lowest price of the security (scaled by `to_int`)                         | security_prices_ohlcv_int      |
| close_price           | INTEGER/REAL   | Closing price of the security (scaled by `to_int`)                        | security_prices_ohlcv_int      |
| volume                | INTEGER   | Trading volume of the security                                            | security_prices_ohlcv_int      |

### Options Tables

| Field Name            | Data Type | Definition                                                                 | Table                          |
|-----------------------|-----------|---------------------------------------------------------------------------|--------------------------------|
| option_ohlcv_id       | INTEGER   | Unique identifier for each option OHLCV record                            | options_ohlcv              |
| underlying_symbol_id  | INTEGER   | Unique identifier for the underlying security                             | options_ohlcv              |
| timestamp_utc_ms      | INTEGER   | Timestamp in UTC milliseconds                                             | options_ohlcv              |
| strike_price      | INTEGER/REAL   | The strike price of the option being tracked (scaled by `to_int`)                                             | options_ohlcv              |
| option_type_id      | INTEGER   | The type of option being tracked, either a put `0` or a call `1`                                            | options_ohlcv              |
| open_price            | INTEGER/REAL   | Opening price of the option (scaled by `to_int`)                          | options_ohlcv              |
| high_price            | INTEGER/REAL   | Highest price of the option (scaled by `to_int`)                          | options_ohlcv              |
| low_price             | INTEGER/REAL  | Lowest price of the option (scaled by `to_int`)                           | options_ohlcv              |
| close_price           | INTEGER/REAL   | Closing price of the option (scaled by `to_int`)                          | options_ohlcv              |
| volume                | INTEGER  | Trading volume of the option                                              | options_ohlcv              |

### Trade Quotes

| Field Name            | Data Type | Definition                                                                 | Table                          |
|-----------------------|-----------|---------------------------------------------------------------------------|--------------------------------|
| quote_id              | INTEGER   | Unique identifier for each quote                                          | security_prices_trade_quotes_int |
| symbol_id             | INTEGER   | Unique identifier for the security                                        | security_prices_trade_quotes_int |
| timestamp_utc_ms      | INTEGER   | Timestamp in UTC milliseconds                                             | security_prices_trade_quotes_int |
| trade_size      | INTEGER   | The number of shares traded                                            | security_prices_trade_quotes_int |
| trade_price      | INTEGER/REAL   | The price at which the security was traded (scaled by `to_int`)                                          | security_prices_trade_quotes_int |
| best_bid_price        | INTEGER/REAL   | Best bid price (scaled by `to_int`)                                       | security_prices_trade_quotes_int |
| best_bid_size         | INTEGER   | Best bid size                                                             | security_prices_trade_quotes_int |
| best_ask_price        | INTEGER/REAL   | Best ask price (scaled by `to_int`)                                       | security_prices_trade_quotes_int |
| best_ask_size         | INTEGER   | Best ask size                                                             | security_prices_trade_quotes_int |
| best_bid_ct           | INTEGER   | Best bid count                                                            | security_prices_trade_quotes_int |
| best_ask_ct           | INTEGER   | Best ask count                                                            | security_prices_trade_quotes_int |

### MBP Full

| Field Name            | Data Type | Definition                                                                 | Table                          |
|-----------------------|-----------|---------------------------------------------------------------------------|--------------------------------|
| quote_id              | INTEGER   | Unique identifier for each quote                                          | security_prices_mbp_full_int   |
| symbol_id             | INTEGER   | Unique identifier for the security                                        | security_prices_mbp_full_int   |
| timestamp_utc         | INTEGER   | Timestamp in UTC                                                          | security_prices_mbp_full_int   |
| action                | INTEGER   | Action type, i.e. trade, cancel, add                                                               | security_prices_mbp_full_int   |
| side                  | INTEGER   | Side of the market (bid/ask)                                              | security_prices_mbp_full_int   |
| size                  | INTEGER   | Size of the order                                                         | security_prices_mbp_full_int   |
| depth                 | INTEGER   | Depth of the market                                                       | security_prices_mbp_full_int   |
| best_bid_price        | INTEGER   | Best bid price (scaled by `to_int`)                                       | security_prices_mbp_full_int   |
| best_bid_size         | INTEGER   | Best bid size                                                             | security_prices_mbp_full_int   |
| best_ask_price        | INTEGER   | Best ask price (scaled by `to_int`)                                       | security_prices_mbp_full_int   |
| best_ask_size         | INTEGER   | Best ask size                                                             | security_prices_mbp_full_int   |
| best_bid_ct           | INTEGER   | Best bid count                                                            | security_prices_mbp_full_int   |
| best_ask_ct           | INTEGER   | Best ask count                                                            | security_prices_mbp_full_int   |

## Securities Metadata

### Cash Table

| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| SymbolID              | INTEGER   | Unique identifier for each security                                       | cash_table           |
| BaseCurrencyID        | INTEGER   | Unique identifier for the base currency                                   | cash_table           |
| QuoteCurrencyID       | INTEGER   | Unique identifier for the quote currency                                  | cash_table           |

### Currencies Table

| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| CurrencyID            | INTEGER   | Unique identifier for each currency                                       | currencies_table     |
| CurrencyAbbr          | TEXT      | Abbreviation of the currency                                              | currencies_table     |

### Equities Snapshots

| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| snapshot_id           | INTEGER   | Unique identifier for each snapshot                                       | equities_snapshots   |
| market_cap            | REAL      | Market capitalization                                                     | equities_snapshots   |
| pe_ratio              | REAL      | Price-to-earnings ratio                                                   | equities_snapshots   |
| eps_ttm               | REAL      | Earnings per share (trailing twelve months)                               | equities_snapshots   |
| dividend_yield        | REAL      | Dividend yield                                                            | equities_snapshots   |
| dividend_per_share    | REAL      | Dividend per share                                                        | equities_snapshots   |
| price_to_book         | REAL      | Price-to-book ratio                                                       | equities_snapshots   |

### ETF Table

| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| symbol_id             | INTEGER   | Unique identifier for each security                                       | etf_table            |
| full_name             | TEXT      | Full name of the ETF                                                      | etf_table            |
| underlying_asset_type_id | INTEGER | Unique identifier for the underlying asset type                           | etf_table            |
| issuer_id             | INTEGER   | Unique identifier for the issuer                                          | etf_table            |
| underlying_asset_name | TEXT      | Name of the underlying asset                                              | etf_table            |

### Fundamentals Snapshots

| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| snapshot_id           | INTEGER   | Unique identifier for each snapshot                                       | fundamentals_snapshots |
| symbol_id             | INTEGER   | Unique identifier for each security                                       | fundamentals_snapshots |
| timestamp_utc_sec     | TEXT      | Timestamp in UTC seconds                                                  | fundamentals_snapshots |

### Futures Table

| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| symbol_id             | INTEGER   | Unique identifier for each security                                       | fut_table            |
| exchange_id           | INTEGER   | Unique identifier for the exchange                                        | fut_table            |
| multiplier            | REAL      | Multiplier value                                                          | fut_table            |
| tick_size             | REAL      | Tick size                                                                 | fut_table            |
| tick_value            | REAL      | Tick value                                                                | fut_table            |
| underlying_asset_type_id | INTEGER | Unique identifier for the underlying asset type                           | fut_table            |
| underlying_asset      | TEXT      | Name of the underlying asset                                              | fut_table            |

### Industry Info

| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| industry_id           | INTEGER   | Unique identifier for each industry                                       | industry_info        |
| industry_name         | TEXT      | Name of the industry                                                      | industry_info        |

### Issuers Table

| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| issuer_id             | INTEGER   | Unique identifier for each issuer                                         | issuers_table        |
| issuer_name           | TEXT      | Name of the issuer                                                        | issuers_table        |

### Mutual Fund Snapshots

| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| snapshot_id           | INTEGER   | Unique identifier for each snapshot                                       | mutual_fund_snapshots |
| nav                   | REAL      | Net asset value                                                           | mutual_fund_snapshots |
| expense_ratio         | REAL      | Expense ratio                                                             | mutual_fund_snapshots |
| ytd_return            | REAL      | Year-to-date return                                                       | mutual_fund_snapshots |

### Sector Info

| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| sector_id             | INTEGER   | Unique identifier for each sector                                         | sector_info          |
| sector_name           | TEXT      | Name of the sector                                                        | sector_info          |

### Stock Splits Table

| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| split_id              | INTEGER   | Unique identifier for each stock split                                    | stock_splits_table   |
| symbol_id             | INTEGER   | Unique identifier for each security                                       | stock_splits_table   |
| splite_timestamp_utc_sec | INTEGER | Timestamp of the stock split in UTC seconds                               | stock_splits_table   |
| share_multiplier      | INTEGER   | Share multiplier value                                                    | stock_splits_table   |

### Stock Table

| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| symbol_id             | INTEGER   | Unique identifier for each security                                       | stk_table            |
| full_name             | TEXT      | Full name of the stock                                                    | stk_table            |
| sp_component          | INTEGER   | S&P 500 component flag                                                    | stk_table            |
| nq_component          | INTEGER   | NASDAQ component flag                                                     | stk_table            |
| djia_component        | INTEGER   | Dow Jones Industrial Average component flag                               | stk_table            |
| rty_component         | INTEGER   | Russell 2000 component flag                                               | stk_table            |
| sector_id             | INTEGER   | Unique identifier for the sector                                          | stk_table            |
| industry_id           | INTEGER   | Unique identifier for the industry                                        | stk_table            |
| ipo_date_utc_sec      | INTEGER   | IPO date in UTC seconds                                                   | stk_table            |

### Underlying Assets Table

| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| underlying_asset_type_id | INTEGER | Unique identifier for each underlying asset type                          | underlying_assets_table |
| underlying_asset_type | TEXT      | Name of the underlying asset type                                         | underlying_assets_table |

## Portfolio Database

### Account Info

| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| account_id            | INTEGER   | Unique identifier for each account                                        | account_info         |
| account_start_timestamp_utc_sec | INTEGER | Account start timestamp in UTC seconds                                   | account_info         |
| account_start_value   | REAL      | Initial value of the account                                              | account_info         |
| account_alias         | TEXT      | Alias for the account                                                     | account_info         |
| paper_trade_flag      | INTEGER   | Flag indicating if the account is for paper trading                       | account_info         |

### All Orders

| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| order_id              | INTEGER   | Unique identifier for each order                                          | all_orders           |
| symbol_id             | INTEGER   | Unique identifier for the security                                        | all_orders           |
| broker_order_id       | INTEGER   | Broker-specific order identifier                                          | all_orders           |
| order_placed_timestamp_utc_ms | INTEGER   | Timestamp when the order was placed in ms using UTC timezone                                    | all_orders           |
| transaction_id        | INTEGER   | Unique identifier for the transaction                                     | all_orders           |
| order_type_id         | INTEGER   | Unique identifier for the order type                                      | all_orders           |
| order_action_id       | INTEGER   | Unique identifier for the order action                                    | all_orders           |
| inference_id          | INTEGER   | Unique identifier for the inference                                       | all_orders           |
| quantity              | INTEGER   | Quantity of the symbol/security in the order                                                     | all_orders           |

### Cancelled Orders

| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| order_id              | INTEGER   | Unique identifier for each order                                          | cancelled_orders     |
| cancelled_timestamp_utc_ms | INTEGER | Timestamp when the order was cancelled in UTC milliseconds                | cancelled_orders     |

### Conditional Orders

| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| order_id              | INTEGER   | Unique identifier for each order                                          | conditional_orders   |
| trigger_price         | REAL      | Trigger price for the conditional order                                   | conditional_orders   |

### Executed Orders

| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| order_id              | INTEGER   | Unique identifier for each order                                          | executed_orders      |
| execution_timestamp_utc_ms | INTEGER | Timestamp when the order was executed in UTC milliseconds                 | executed_orders      |
| execution_price       | REAL      | Execution price of the order                                              | executed_orders      |
| fees                  | REAL      | Fees associated with the order                                            | executed_orders      |

### Inference Steps

| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| inference_step_id     | INTEGER   | Unique identifier for each inference step                                 | inference_steps      |
| module_id             | INTEGER   | Unique identifier for the module                                          | inference_steps      |
| step_name             | TEXT      | Name of the inference step                                                | inference_steps      |

### Inference Times

| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| inference_step_timing_id | INTEGER | Unique identifier for each inference step timing                          | inference_times      |
| inference_id          | INTEGER   | Unique identifier for the inference                                       | inference_times      |
| inference_step_id     | INTEGER   | Unique identifier for the inference step                                  | inference_times      |
| step_start_timestamp_utc_ms | INTEGER | Start timestamp of the inference step in UTC milliseconds                 | inference_times      |
| step_end_timestamp_utc_ms | INTEGER | End timestamp of the inference step in UTC milliseconds                   | inference_times      |

### Inferences

| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| inference_id          | INTEGER   | Unique identifier for each inference                                      | inferences           |
| symbol_id             | INTEGER   | Unique identifier for the security                                        | inferences           |
| strategy_id           | INTEGER   | Unique identifier for the strategy                                        | inferences           |
| session_id            | INTEGER   | Unique identifier for the session                                         | inferences           |
| inference_outputs     | INTEGER   | Outputs of the inference                                                  | inferences           |
| inference_start_timestamp_utc_ms | INTEGER | Start timestamp of the inference in UTC milliseconds                      | inferences           |
| inference_end_timestamp_utc_ms | INTEGER | End timestamp of the inference in UTC milliseconds                        | inferences           |
| candle_reference_timestamp_utc_sec | INTEGER | Reference timestamp of the candle in UTC seconds                          | inferences           |

### Model Libraries

| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| model_library_id      | INTEGER   | Unique identifier for each model library                                  | model_libraries      |
| model_library         | TEXT      | Name of the model library such as sci-kit learn or pytorch                                            | model_libraries      |

### Model Types

| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| model_type_id         | INTEGER   | Unique identifier for each model type                                     | model_types          |
| model_type            | TEXT      | Name of the model type such as `StandardScaler`                                                    | model_types          |
| model_library_id      | INTEGER   | Unique identifier for the model library                                   | model_types          |

### Models

| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| model_id              | INTEGER   | Unique identifier for each model                                          | models               |
| strategy_id           | INTEGER   | Unique identifier for the strategy                                        | models               |
| model_name            | TEXT      | Name of the model                                                         | models               |
| model_type_id         | INTEGER   | Unique identifier for the model type                                      | models               |
| model_dvc_hash        | TEXT      | DVC hash of the model                                                     | models               |

### Order Actions

| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| order_action_id       | INTEGER   | Unique identifier for each order action                                   | order_actions        |
| order_action          | TEXT      | Name of the order action such as `Buy` or `Sell`                                                  | order_actions        |

### Order Types

| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| order_type_id         | INTEGER   | Unique identifier for each order type                                     | order_types          |
| order_type            | TEXT      | Name of the order type such as `Stop`, `Limit`, or `Market`                                                    | order_types          |

### Sessions

| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| session_id            | INTEGER   | Unique identifier for each session                                        | sessions             |
| created_timestamp_utc_ms | INTEGER | Timestamp when the session was created in UTC milliseconds                | sessions             |
| ended_timestamp_utc_ms         | INTEGER   | Timestamp when the session ended in UTC milliseconds                                      | sessions             |

### Strategies

| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| strategy_id           | INTEGER   | Unique identifier for each strategy                                       | strategies           |
| strategy_name         | TEXT      | Name of the strategy                                                      | strategies           |
| strategy_version      | TEXT      | Version of the strategy, should follow semantic versioning but this is not enforced                                                   | strategies           |
| strategy_description  | TEXT      | Description of the strategy (optional)                                               | strategies           |

### Strategy Modules
This useful if your strategy requires multiple python modules, can help with debugging and useful for tracking inference times and grouping inference steps into related groups
| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| module_id             | INTEGER   | Unique identifier for each module                                         | strategy_modules     |
| strategy_id           | INTEGER   | Unique identifier for the strategy                                        | strategy_modules     |
| module_name           | TEXT      | Name of the module                                                        | strategy_modules     |

### Transaction Types

| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| transaction_type_id   | INTEGER   | Unique identifier for each transaction type                               | transaction_types    |
| transaction_type      | TEXT      | Name of the transaction type such as `cancelled_order`, `dividend_payment`, `cash_infusion  `                                              | transaction_types    |

### Transactions

| Field Name            | Data Type | Definition                                                                 | Table                |
|-----------------------|-----------|---------------------------------------------------------------------------|----------------------|
| transaction_id        | INTEGER   | Unique identifier for each transaction                                    | transactions         |
| account_id            | INTEGER   | Unique identifier for the account                                         | transactions         |
| transaction_type_id   | INTEGER   | Unique identifier for the transaction type                                | transactions         |
| transaction_timestamp_utc_ms | INTEGER | Timestamp of the transaction in UTC milliseconds                         | transactions         |
| transaction_value     | REAL      | Value of the transaction                                                  | transactions         |
