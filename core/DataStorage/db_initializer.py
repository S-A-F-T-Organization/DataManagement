import config
import sqlalchemy
import yaml

class DBInitializer:

    def __init__(self):
        # Read in YAML configuration files
        with open('config/database_config_template.yml', 'r') as f:
            self.db_info = yaml.safe_load('database')
            self.market_data_flag = yaml.safe_load('schemas')[0]
            self.portfolio_data_flag = yaml.safe_load('schemas')[1]
            self.security_types = yaml.safe_load('security_types')
            self.seed_data = yaml.safe_load('seed_data')
    
    def initialize_database(config):
        # Connect to DB
        sqlalchemy.conn
        # Always create shared base tables (e.g., dim_Securities, fact_Prices, etc.)
        run_sql_script('create_market_data_tables/00_base_tables.sql', conn)

        # Now check user choices for security types
        if config['security_types'].get('equities', False):
            run_sql_script('create_market_data_tables/01_create_equities_tables.sql', conn)

        if config['security_types'].get('futures', False):
            run_sql_script('create_market_data_tables/02_create_futures_tables.sql', conn)

        if config['security_types'].get('bonds', False):
            run_sql_script('create_market_data_tables/03_create_bonds_tables.sql', conn)

        ...

        # Optionally run seed data for each type as well
        if config['seed_data'].get('security_types'):
            # For instance, insert only the chosen ones:
            if config['security_types'].get('equities', False):
                run_sql_script('seed_data/equities_insert.sql', conn)
            if config['security_types'].get('futures', False):
                run_sql_script('seed_data/futures_insert.sql', conn)
        ...
