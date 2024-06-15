from gmx.utils import ConfigManager
from gmx.stats import GMXv2Stats


to_json = True
to_csv = True

config = ConfigManager(chain='arbitrum')
config.set_config()

stats_object = GMXv2Stats(
    config=config,
    to_json=to_json,
    to_csv=to_csv
)

markets = stats_object.get_available_markets()
liquidity = stats_object.get_available_liquidity()
borrow_apr = stats_object.get_borrow_apr()
claimable_fees = stats_object.get_claimable_fees()
contract_tvl = stats_object.get_contract_tvl()
funding_apr = stats_object.get_funding_apr()
gm_prices = stats_object.get_gm_price()
open_interest = stats_object.get_open_interest()
oracle_prices = stats_object.get_oracle_prices()
pool_tvl = stats_object.get_pool_tvl()
