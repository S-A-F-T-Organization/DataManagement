from sqlalchemy import create_engine
import yaml
import logging

class DBInitializer:
    """
    This class manages the initialization of the database as specified in the user's config file

    Parameters:
    - config_path(optional[str]): The path to the users config file. If setup correctly it should not be needed so it is optional. If the user runs into problems they can specify the path to their config file.
    """

    def __init__(self, config_path:str='config/my_config.yml'):
        # Setup logger/stream handler
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(messages)s'
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        # Read in the config file information
        try:
            # Read in YAML configuration files
            with open(f'{config_path}', 'r') as f:
                self.config_data = yaml.safe_load(f)
                self.db_info = self.config_data['database']
                self.market_data_flag = self.config_data['schemas']['market_data']
                self.portfolio_data_flag = self.config_data['schemas']['portfolio_data']
                self.to_int_flag = self.config_data['schemas']['convert_price_to_int']
                self.security_types = self.config_data['security_types']
                self.seed_data = self.config_data['seed_data']
        except FileNotFoundError as fe:
            self.logger.error("Could not find configuration file: %s", fe)
            raise
        except Exception as e:
            self.logger.error('Error reading the configuration file %s', e)
            raise
    
    def initialize_orm(self):
        self.engine = create_engine(self.db_info[2])
        return None
    
    # def initialize_database(config):
        # # Connect to DB
        
        # # Always create shared base tables (e.g., dim_Securities, fact_Prices, etc.)
        # run_sql_script('create_market_data_tables/00_base_tables.sql', conn)

        # # Now check user choices for security types
        # if config['security_types'].get('equities', False):
        #     run_sql_script('create_market_data_tables/01_create_equities_tables.sql', conn)

        # if config['security_types'].get('futures', False):
        #     run_sql_script('create_market_data_tables/02_create_futures_tables.sql', conn)

        # if config['security_types'].get('bonds', False):
        #     run_sql_script('create_market_data_tables/03_create_bonds_tables.sql', conn)

        # ...

        # # Optionally run seed data for each type as well
        # if config['seed_data'].get('security_types'):
        #     # For instance, insert only the chosen ones:
        #     if config['security_types'].get('equities', False):
        #         run_sql_script('seed_data/equities_insert.sql', conn)
        #     if config['security_types'].get('futures', False):
        #         run_sql_script('seed_data/futures_insert.sql', conn)
        ...
