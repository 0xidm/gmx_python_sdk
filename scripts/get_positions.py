from decimal import Decimal

from gmx.data.markets import Markets
from gmx.data.open_positions import transform_open_position_to_order_parameters, get_positions
from gmx.utils import ConfigManager


if __name__ == "__main__":

    config = ConfigManager(chain='arbitrum')
    config.set_config()

    positions = get_positions(
        config=config,
        address=None
    )

    market_symbol = "ETH"
    is_long = True

    out_token = "USDC"
    amount_of_position_to_close = 1
    amount_of_collateral_to_remove = 1

    order_params = transform_open_position_to_order_parameters(
        config=config,
        positions=positions,
        market_symbol=market_symbol,
        is_long=is_long,
        slippage_percent=0.003,
        out_token="USDC",
        amount_of_position_to_close=amount_of_position_to_close,
        amount_of_collateral_to_remove=amount_of_collateral_to_remove
    )
