from .data.available_liquidity import GetAvailableLiquidity
from .data.borrow_apr import GetBorrowAPR
from .data.claimable_fees import GetClaimableFees
from .data.contract_balance import GetPoolTVL as ContractTVL
from .data.funding_apr import GetFundingFee
from .data.gm_prices import GMPrices
from .data.markets import Markets
from .data.open_interest import OpenInterest
from .data.oracle_prices import OraclePrices
from .data.pool_tvl import GetPoolTVL


class GMXv2Stats:
    def __init__(self, config, to_json, to_csv):
        self.config = config
        self.to_json = to_json
        self.to_csv = to_csv

    def get_available_liquidity(self):

        return GetAvailableLiquidity(
            self.config
        ).get_data(
            to_csv=self.to_csv,
            to_json=self.to_json
        )

    def get_borrow_apr(self):

        return GetBorrowAPR(
            self.config
        ).get_data(
            to_csv=self.to_csv,
            to_json=self.to_json
        )

    def get_claimable_fees(self):

        return GetClaimableFees(
            self.config
        ).get_data(
            to_csv=self.to_csv,
            to_json=self.to_json
        )

    def get_contract_tvl(self):

        return ContractTVL(
            self.config
        ).get_pool_balances(
            to_json=self.to_json
        )

    def get_funding_apr(self):

        return GetFundingFee(
            self.config
        ).get_data(
            to_csv=self.to_csv,
            to_json=self.to_json
        )

    def get_gm_price(self):

        return GMPrices(
            self.config
        ).get_price_traders(
            to_csv=self.to_csv,
            to_json=self.to_json
        )

    def get_available_markets(self):

        return Markets(
            self.config
        ).get_available_markets()

    def get_open_interest(self):

        return OpenInterest(
            self.config
        ).get_data(
            to_csv=self.to_csv,
            to_json=self.to_json
        )

    def get_oracle_prices(self):

        return OraclePrices(
            self.config.chain
        ).get_recent_prices()

    def get_pool_tvl(self):

        return GetPoolTVL(
            self.config
        ).get_pool_balances(
            to_csv=self.to_csv,
            to_json=self.to_json
        )
