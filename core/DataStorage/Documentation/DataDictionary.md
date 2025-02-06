# Data Dictionary

Below is the data dictionary for the tables based on the provided SQL definitions.

## Table of Contents

## Core Tables
### SecuritiesInfo
| Column         | Data Type                                | Description                                                                 |
|----------------|-------------------------------------------|-----------------------------------------------------------------------------|
| SymbolID       | INTEGER PRIMARY KEY AUTO_INCREMENT        | Unique identifier for each security. Automatically increments.              |
| SecurityTypeID | INTEGER NOT NULL                          | References the security type (from `SecurityTypes` table).                  |
| ToInt          | INTEGER NOT NULL                          | Indicates whether the price data is stored as an integer (1) or not (0).    |
| ExchangeID     | INTEGER NOT NULL                          | References the exchange (from `SecurityExchanges` table).                   |
| RTHStartTime   | TEXT                                      | Regular trading hours start time for the security.                          |
| RTHEndTime     | TEXT                                      | Regular trading hours end time for the security.                            |

### SecurityPrices
| Column     | Data Type        | Description                                                                                                     |
|------------|------------------|-----------------------------------------------------------------------------------------------------------------|
| SymbolID   | INTEGER NOT NULL | References the `SymbolID` in `SecuritiesInfo`, linking the price record to a specific security.                |
| DateTime   | INTEGER NOT NULL | The date-time (often Unix epoch or another integer-based time format) indicating when the price data was recorded. |
| OpenPrice  | INTEGER NOT NULL | The opening price for the specific time interval. Stored as an integer if `ToInt` is set to 1.                  |
| HighPrice  | INTEGER NOT NULL | The highest price for the time interval. Stored as an integer if `ToInt` is set to 1.                           |
| LowPrice   | INTEGER NOT NULL | The lowest price for the time interval. Stored as an integer if `ToInt` is set to 1.                            |
| ClosePrice | INTEGER NOT NULL | The closing price for the time interval. Stored as an integer if `ToInt` is set to 1.                           |
| Volume     | INTEGER NOT NULL | The trading volume for the time interval.                                                                       |

### SecurityTypes
| Column         | Data Type                                 | Description                                                                      |
|----------------|--------------------------------------------|----------------------------------------------------------------------------------|
| SecurityTypeID | INTEGER PRIMARY KEY AUTO_INCREMENT         | Unique identifier for the security type. Automatically increments.               |
| SecurityType   | TEXT NOT NULL                              | The name or code representing a type of security (e.g., 'STK', 'ETF', etc.).     |

### SecurityExchanges
| Column      | Data Type                                 | Description                                                                      |
|-------------|--------------------------------------------|----------------------------------------------------------------------------------|
| ExchangeID  | INTEGER PRIMARY KEY AUTO_INCREMENT         | Unique identifier for the exchange. Automatically increments.                    |
| Exchange    | TEXT NOT NULL                              | The name or code representing an exchange (e.g., 'NYSE', 'NASDAQ', etc.).        |

## Market Data Tables
### FX/Cash Tables
#### ForexMetadata
| Column          | Data Type              | Description                                                                             |
|-----------------|------------------------|-----------------------------------------------------------------------------------------|
| SymbolID        | INTEGER PRIMARY KEY   | Unique identifier for this Forex entry. Potentially the same as `SymbolID` in `SecuritiesInfo`. |
| BaseCurrencyID  | INTEGER               | The `CurrencyID` of the base currency for the Forex pair (references `Currencies`).     |
| QuoteCurrencyID | INTEGER               | The `CurrencyID` of the quote currency for the Forex pair (references `Currencies`).    |

#### Currencies
| Column       | Data Type                             | Description                                                           |
|--------------|----------------------------------------|-----------------------------------------------------------------------|
| CurrencyID   | INTEGER PRIMARY KEY AUTO_INCREMENT     | Unique identifier for the currency, auto-incremented.                 |
| CurrencyAbbr | TEXT                                   | The currency abbreviation (e.g., 'USD', 'EUR').                       |

### ETF Tables

#### ETFMetadata
| Column                | Data Type              | Description                                                                                                 |
|-----------------------|------------------------|-------------------------------------------------------------------------------------------------------------|
| SymbolID              | INTEGER PRIMARY KEY    | Unique identifier for this ETF entry (typically the same `SymbolID` from `SecuritiesInfo`).                |
| FullName              | TEXT                   | The full name of the ETF.                                                                                  |
| UnderlyingAssetTypeID | INTEGER                | Identifier for the underlying asset type.                                                                  |
| IssuerID              | INTEGER                | References the issuer of this ETF (from `Issuers`).                                                        |
| UnderlyingAsset       | TEXT                   | A description or identifier of the underlying asset(s) that the ETF tracks.                                |

#### Issuers
| Column      | Data Type                             | Description                                                  |
|-------------|----------------------------------------|--------------------------------------------------------------|
| IssuerID    | INTEGER PRIMARY KEY AUTO_INCREMENT     | Unique identifier for the issuer (auto-incremented).         |
| IssuerName  | TEXT                                   | The name of the entity issuing the ETF or other security.    |

### Stocks Tables

#### StockMetadata
| Column       | Data Type           | Description                                                                                                 |
|--------------|---------------------|-------------------------------------------------------------------------------------------------------------|
| SymbolID     | INTEGER PRIMARY KEY | Unique identifier for the stock (same as `SymbolID` from `SecuritiesInfo`).                                |
| FullName     | TEXT                | The full name of the stock or company.                                                                      |
| SPComponent  | INTEGER             | Indicates if the stock is part of the S&P index (1 = yes, 0 = no).                                          |
| NQComponent  | INTEGER             | Indicates if the stock is part of the Nasdaq index (1 = yes, 0 = no).                                       |
| DJComponent  | INTEGER             | Indicates if the stock is part of the Dow Jones index (1 = yes, 0 = no).                                    |
| RTYComponent | INTEGER             | Indicates if the stock is part of the Russell 2000 index (1 = yes, 0 = no).                                 |
| VIXComponent | INTEGER             | Indicates if the stock is included in the VIX calculation (1 = yes, 0 = no).                                |
| SectorID     | INTEGER             | References the sector (from `StockSectors`).                                                               |
| IndustryID   | INTEGER             | References the industry (from `StockIndustries`).                                                          |
| IPODate      | TEXT                | The date the company had its IPO (Initial Public Offering).                                                |

#### StockSectors
| Column    | Data Type                             | Description                                              |
|-----------|----------------------------------------|----------------------------------------------------------|
| SectorID  | INTEGER PRIMARY KEY AUTO_INCREMENT     | Unique identifier for the stock sector.                  |
| SectorName| TEXT                                   | The name of the sector (e.g., Technology, Finance).      |

#### StockIndustries
| Column      | Data Type                             | Description                                                  |
|-------------|----------------------------------------|--------------------------------------------------------------|
| IndustryID  | INTEGER PRIMARY KEY AUTO_INCREMENT     | Unique identifier for the stock industry.                    |
| IndustryName| TEXT                                   | The name of the industry (e.g., Software, Banking).          |

#### FundamentalSnapshots
| Column    | Data Type           | Description                                                                                                       |
|-----------|---------------------|-------------------------------------------------------------------------------------------------------------------|
| SymbolID  | INTEGER PRIMARY KEY | Unique identifier for the security (same as `SymbolID` in `SecuritiesInfo`).                                      |
| DateTime  | TEXT                | Timestamp or date when the fundamental snapshot was taken.                                                        |
| MarketCap | REAL                | The total market capitalization of the security at the given DateTime.                                            |

### Shared Equities Tables

#### DividendHistory
| Column    | Data Type           | Description                                                                                                       |
|-----------|---------------------|-------------------------------------------------------------------------------------------------------------------|
| SymbolID  | INTEGER PRIMARY KEY | Unique identifier for the security (same as `SymbolID` in `SecuritiesInfo`).                                      |
| DateTime  | TEXT                | Timestamp or date when the dividend was declared or paid.                                                         |
| Dividend  | REAL                | The dividend amount paid per share.                                                                               |

#### EarningsHistory
| Column    | Data Type           | Description                                                                                                        |
|-----------|---------------------|--------------------------------------------------------------------------------------------------------------------|
| SymbolID  | INTEGER PRIMARY KEY | Unique identifier for the security (same as `SymbolID` in `SecuritiesInfo`).                                       |
| DateTime  | TEXT                | The date/time for which the earnings are recorded (e.g., an earnings release date).                                |
| Earnings  | REAL                | The earnings figure (could be earnings per share or total, depending on use case).                                 |

#### StockSplits
| Column    | Data Type           | Description                                                                                                      |
|-----------|---------------------|------------------------------------------------------------------------------------------------------------------|
| SymbolID  | INTEGER PRIMARY KEY | Unique identifier for the security (same as `SymbolID` in `SecuritiesInfo`).                                    |
| DateTime  | TEXT                | The date/time the stock split occurred.                                                                          |
| Split     | REAL                | The split ratio (e.g., 2.0 for a 2-for-1 split, 0.5 for a 1-for-2 reverse split).                                 |

### Other Market Data Tables

#### UnderlyingAssetTypes
| Column               | Data Type                             | Description                                                                       |
|----------------------|----------------------------------------|-----------------------------------------------------------------------------------|
| UnderlyingAssetTypeID| INTEGER PRIMARY KEY AUTO_INCREMENT     | Unique identifier for the underlying asset type (auto-incremented).               |
| UnderlyingAssetType  | TEXT NOT NULL                          | A textual identifier for the asset type (e.g., 'Commodity', 'Equity', 'Bond').    |

## Portfolio Analysis Tables

### AllOrdersTable
| Column         | Data Type           | Description                                                                                      |
|----------------|---------------------|--------------------------------------------------------------------------------------------------|
| TransactionID  | INTEGER PRIMARY KEY | Unique identifier for the order transaction.                                                    |
| PlacedDatetime | INTEGER            | The date/time (often epoch) the order was placed.                                                |
| SymbolID       | INTEGER            | References the security (e.g., `SymbolID` in `SecuritiesInfo`).                                  |
| OrderType      | TEXT               | The type of order (e.g., 'Market', 'Limit', etc.).                                               |
| StrategyID     | INTEGER            | References a strategy in `StrategyInfoTable` to indicate the strategy that generated this order.  |
| SessionID      | INTEGER            | References the session (from `SessionTable`).                                                    |
| InferenceID    | INTEGER            | References the inference (from `ModelInferenceTable`) if generated by a model.                   |

### CanceledOrdersTable
| Column          | Data Type           | Description                                                                         |
|-----------------|---------------------|-------------------------------------------------------------------------------------|
| TransactionID   | INTEGER PRIMARY KEY | The transaction ID of the order that was canceled (references `AllOrdersTable`).    |
| CanceledDatetime| INTEGER            | The date/time the order was canceled.                                               |

### ExecutedOrdersTable
| Column          | Data Type           | Description                                                                        |
|-----------------|---------------------|------------------------------------------------------------------------------------|
| TransactionID   | INTEGER PRIMARY KEY | The transaction ID of the order that was executed (references `AllOrdersTable`).  |
| ExecutedDatetime| INTEGER            | The date/time the order was executed.                                             |
| ExecutionPrice  | REAL                | The price at which the order was filled.                                          |
| Fees            | REAL                | The fees associated with executing the order.                                     |

### TransactionsTable
| Column             | Data Type                             | Description                                                                         |
|--------------------|----------------------------------------|-------------------------------------------------------------------------------------|
| TransactionID      | INTEGER PRIMARY KEY AUTO_INCREMENT     | Unique identifier for the financial transaction. Automatically increments.          |
| AccountID          | INTEGER                                | References the account (from `AccountSummaryTable`).                                |
| TransactionTypeID  | INTEGER                                | References the transaction type (from `TransactionTypesTable`).                     |
| TransactionDatetime| INTEGER                                | The date/time when the transaction occurred.                                        |
| TransactionValue   | REAL                                   | The monetary value of the transaction.                                              |

### AccountSummaryTable
| Column              | Data Type           | Description                                                                  |
|---------------------|---------------------|------------------------------------------------------------------------------|
| AccountID           | INTEGER PRIMARY KEY | Unique identifier for the account.                                           |
| AccountStartDatetime| INTEGER            | The date/time the account was initially created or funded.                   |
| AccountStartValue   | REAL                | The initial value (balance) of the account.                                  |
| AccountAlias        | TEXT                | A user-friendly alias or name for the account.                               |

### TransactionTypesTable
| Column           | Data Type                             | Description                                                    |
|------------------|----------------------------------------|----------------------------------------------------------------|
| TransactionTypeID| INTEGER PRIMARY KEY AUTO_INCREMENT     | Unique identifier for the transaction type. Auto-incremented.  |
| TransactionType  | TEXT                                   | A textual label for the transaction type (e.g., 'Deposit').     |

### SessionTable
| Column                | Data Type                             | Description                                                    |
|-----------------------|----------------------------------------|----------------------------------------------------------------|
| SessionID             | INTEGER PRIMARY KEY AUTO_INCREMENT     | Unique identifier for the session. Automatically increments.   |
| DatetimeCreated       | INTEGER                                | The date/time the session was created.                         |
| DatetimeEnded         | INTEGER                                | The date/time the session ended (if applicable).               |
| DataReaderStartDatetime| INTEGER                               | The date/time data reading began (if relevant).                |

### ModelInferenceTable
| Column               | Data Type           | Description                                                                              |
|----------------------|---------------------|------------------------------------------------------------------------------------------|
| InferenceID          | INTEGER PRIMARY KEY | Unique identifier for the inference.                                                    |
| SymbolID             | INTEGER            | References the security (e.g., `SymbolID` in `SecuritiesInfo`).                         |
| PredictedSentiment   | INTEGER            | Stores a sentiment label or category (e.g., 1 = positive, -1 = negative, 0 = neutral).   |
| InferenceStartDatetime| INTEGER            | The date/time the inference process started.                                            |
| InferenceEndDatetime  | INTEGER            | The date/time the inference process ended.                                              |
| ConfidenceLevel       | REAL               | The confidence or probability associated with the inference.                            |
| ReferenceTimestamp    | INTEGER            | A reference date/time used in the inference (e.g., data snapshot time).                |

### StrategyInfoTable
| Column         | Data Type                             | Description                                                    |
|----------------|----------------------------------------|----------------------------------------------------------------|
| StrategyID     | INTEGER PRIMARY KEY AUTO_INCREMENT     | Unique identifier for the strategy. Auto-incremented.          |
| StrategyName   | TEXT                                   | The name of the strategy (e.g., 'Mean Reversion Strategy').    |
| StrategyVersion| REAL                                   | The version number of the strategy (e.g., 1.0, 2.0).           |