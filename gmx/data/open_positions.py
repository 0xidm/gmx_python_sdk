import logging
import numpy as np

from . import GetData
from .oracle_prices import OraclePrices
from ..utils import get_tokens_address_dict, convert_to_checksum_address, find_dictionary_by_key_value, determine_swap_route


chain = 'arbitrum'


class GetOpenPositions(GetData):
    def __init__(self, config: str, address: str):
        super().__init__(config)
        self.address = convert_to_checksum_address(config, address)

    def get_data(self):
        """
        Get all open positions for a given address on the chain defined in
        class init

        Parameters
        ----------
        address : str
            evm address .

        Returns
        -------
        processed_positions : dict
            a dictionary containing the open positions, where asset and
            direction are the keys.

        """
        raw_positions = self.reader_contract.functions.getAccountPositions(
            self.data_store_contract_address,
            self.address,
            0,
            10
        ).call()

        if len(raw_positions) == 0:
            logging.info(
                'No positions open for address: "{}"" on {}.'.format(
                    address,
                    self.config.chain.title()
                )
            )
        processed_positions = {}

        for raw_position in raw_positions:
            processed_position = self._get_data_processing(raw_position)

            # TODO - maybe a better way of building the key?
            if processed_position['is_long']:
                direction = 'long'
            else:
                direction = 'short'

            key = "{}_{}".format(
                processed_position['market_symbol'][0],
                direction
            )
            processed_positions[key] = processed_position

        return processed_positions

    def _get_data_processing(self, raw_position: tuple):
        """
        A tuple containing the raw information return from the reader contract
        query GetAccountPositions

        Parameters
        ----------
        raw_position : tuple
            raw information return from the reader contract .

        Returns
        -------
        dict
            a processed dictionary containing info on the positions.
        """
        market_info = self.markets.info[raw_position[0][1]]

        chain_tokens = get_tokens_address_dict(chain)

        entry_price = (
            raw_position[1][0] / raw_position[1][1]
        ) / 10 ** (
            30 - chain_tokens[market_info['index_token_address']]['decimals']
        )

        leverage = (
            raw_position[1][0] / 10 ** 30
        ) / (
            raw_position[1][2] / 10 ** chain_tokens[
                raw_position[0][2]
            ]['decimals']
        )
        prices = OraclePrices(chain=chain).get_recent_prices()
        mark_price = np.median(
            [
                float(
                    prices[market_info['index_token_address']]['maxPriceFull']
                ),
                float(
                    prices[market_info['index_token_address']]['minPriceFull']
                )
            ]
        ) / 10 ** (
            30 - chain_tokens[market_info['index_token_address']]['decimals']
        )

        return {
            "account": raw_position[0][0],
            "market": raw_position[0][1],
            "market_symbol": (
                self.markets.info[raw_position[0][1]]['market_symbol'],
            ),
            "collateral_token": chain_tokens[raw_position[0][2]]['symbol'],
            "position_size": raw_position[1][0] / 10**30,
            "size_in_tokens": raw_position[1][1],
            "entry_price": (
                (
                    raw_position[1][0] / raw_position[1][1]
                ) / 10 ** (
                    30 - chain_tokens[
                        market_info['index_token_address']
                    ]['decimals']
                )
            ),
            "inital_collateral_amount": raw_position[1][2],
            "inital_collateral_amount_usd": (
                raw_position[1][2]
                / 10 ** chain_tokens[raw_position[0][2]]['decimals'],
            ),
            "leverage": leverage,
            "borrowing_factor": raw_position[1][3],
            "funding_fee_amount_per_size": raw_position[1][4],
            "long_token_claimable_funding_amount_per_size": raw_position[1][5],
            "short_token_claimable_funding_amount_per_size": raw_position[1][6],
            "position_modified_at": "",
            "is_long": raw_position[2][0],
            "percent_profit": (
                (
                    1 - (mark_price / entry_price)
                ) * leverage
            ) * 100,
            "mark_price": mark_price
        }

def transform_open_position_to_order_parameters(
    config,
    positions: dict,
    market_symbol: str,
    is_long: bool,
    slippage_percent: float,
    out_token,
    amount_of_position_to_close,
    amount_of_collateral_to_remove
):
    """
    Find the user defined trade from market_symbol and is_long in a dictionary
    positions and return a dictionary formatted correctly to close 100% of
    that trade

    Parameters
    ----------
    chain : str
        arbitrum or avalanche.
    positions : dict
        dictionary containing all open positions.
    market_symbol : str
        symbol of market trader.
    is_long : bool
        True for long, False for short.
    slippage_percent : float
        slippage tolerance to close trade as a percentage.

    Raises
    ------
    Exception
        If we can't find the requested trade for the user.

    Returns
    -------
    dict
        order parameters formatted to close the position.

    """
    direction = "short"
    if is_long:
        direction = "long"

    position_dictionary_key = "{}_{}".format(
        market_symbol.upper(),
        direction
    )

    try:
        raw_position_data = positions[position_dictionary_key]
        gmx_tokens = get_tokens_address_dict(config.chain)

        collateral_address = find_dictionary_by_key_value(
            gmx_tokens,
            "symbol",
            raw_position_data['collateral_token']
        )["address"]

        gmx_tokens = get_tokens_address_dict(config.chain)

        index_address = find_dictionary_by_key_value(
            gmx_tokens,
            "symbol",
            raw_position_data['market_symbol'][0]
        )
        out_token_address = find_dictionary_by_key_value(
            gmx_tokens,
            "symbol",
            out_token
        )['address']
        markets = Markets(config=config).get_available_markets()

        swap_path = []

        if collateral_address != out_token_address:
            swap_path = determine_swap_route(
                markets,
                collateral_address,
                out_token_address
            )[0]
        size_delta = int(int(
            (Decimal(raw_position_data['position_size']) * (Decimal(10)**30))
        ) * amount_of_position_to_close)

        return {
            "chain": config.chain,
            "market_key": raw_position_data['market'],
            "collateral_address": collateral_address,
            "index_token_address": index_address["address"],
            "is_long": raw_position_data['is_long'],
            "size_delta": size_delta,
            "initial_collateral_delta": int(int(
                raw_position_data['inital_collateral_amount']
            ) * amount_of_collateral_to_remove
            ),
            "slippage_percent": slippage_percent,
            "swap_path": swap_path
        }
    except KeyError:
        raise Exception(
            "Couldn't find a {} {} for given user!".format(
                market_symbol, direction
            )
        )

def get_positions(config, address: str = None):
    """
    Get open positions for an address on a given network.
    If address is not passed it will take the address from the users config
    file.

    Parameters
    ----------
    chain : str
        arbitrum or avalanche.
    address : str, optional
        address to fetch open positions for. The default is None.

    Returns
    -------
    positions : dict
        dictionary containing all open positions.

    """

    if address is None:
        address = config.user_wallet_address
        if address is None:
            raise Exception("No address passed in function or config!")

    positions = GetOpenPositions(config=config, address=address).get_data()

    if len(positions) > 0:
        print("Open Positions for {}:".format(address))
        for key in positions.keys():
            print(key)

    return positions
