import click
from core.ETLs import market_data_etl, portfolio_etl

@click.group()
def cli():
    pass

@cli.command()
@click.option('--start-date', required=True)
@click.option('--end-date', required=True)
def run_market_data_etl(start_date, end_date):
    # parse config, run ETL
    market_data_etl.run(start_date, end_date)

@cli.command()
def run_portfolio_etl():
    portfolio_etl.run()

if __name__ == '__main__':
    cli()
