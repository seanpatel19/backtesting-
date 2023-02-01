from zipline.pipeline import Pipeline
from zipline.pipeline.engine import SimplePipelineEngine
from zipline.pipeline.factors import AverageDollarVolume
from zipline.utils.calendars import get_calendar
from zipline.pipeline.loaders import USEquityPricingLoader
from zipline.data.data_portal import DataPortal

# Bid/Ask spread for Top 500 liquid US stocks are 2-5bp. Less than 10bp is inevitable to achieve 400bp p.a. level of return from daily trade of 
universe = AverageDollarVolume(window_length=120).top(500)

# Use NYSE Caleander 
trading_calendar = get_calendar('NYSE')

# Define Loader for US Equity Price
pricing_loader = USEquityPricingLoader(bundle_data.equity_daily_bar_reader, bundle_data.adjustment_reader)

# Create a DataPortal for convenience
data_portal = DataPortal(bundle_data.asset_finder, trading_calendar=trading_calendar, first_trading_day=bundle_data.equity_daily_bar_reader.first_trading_day, equity_minute_reader=None, equity_daily_reader=bundle_data.equity_daily_bar_reader, adjustment_reader=bundle_data.adjustment_reader)

# Create Engine
engine = SimplePipelineEngine(get_loader=pricing_loader.get_loader, calendar=trading_calendar.all_sessions, asset_finder=bundle_data.asset_finder)

# Get universe tickers
universe_end_date = pd.Timestamp('2016-01-05', tz='UTC')
universe_tickers = engine.run_pipeline(Pipeline(screen=universe), universe_end_date, universe_end_date).index.get_level_values(1).values.tolist()

# Returns
start_dt = pd.Timestamp((universe_end_date - pd.DateOffset(years=5, days=1)).strftime('%Y-%m-%d'), tz='UTC', freq='C')
end_dt = pd.Timestamp(universe_end_date.strftime('%Y-%m-%d'), tz='UTC', freq='C')

start_loc = trading_calendar.closes.index.get_loc(start_dt)
end_loc = trading_calendar.closes.index.get_loc(end_dt)

five_year_returns = data_portal.get_history_window(assets=universe_tickers, end_dt=end_dt, bar_count=end_loc - start_loc, frequency='1d', field='close', data_frequency='daily')\
    .pct_change()[1:].fillna(0)