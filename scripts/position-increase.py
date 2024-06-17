from gmx.order.parser import OrderArgumentParser
from gmx.order.position import IncreaseOrder
from gmx.utils import ConfigManager


# Example of passing arguments through the Order parser to increase the desired position

parameters = {
    "chain": 'arbitrum',

    # the market you want to trade on
    "index_token_symbol": "BTC",

    # token to use as collateral. Start token swaps into collateral token if different
    "collateral_token_symbol": "BTC",

    # the token to start with - WETH not supported yet
    "start_token_symbol": "BTC",

    # True for long, False for short
    "is_long": True,

    # leveraged size of your position; in USD
    "size_delta_usd": 5,

    # if leverage is passed, will calculate number of tokens in start_token_symbol amount
    "leverage": 1,

    # # amount of tokens NOT USD you want to remove as collateral.
    # "initial_collateral_delta": 0.027,

    # as a decimal ie 0.003 == 0.3%
    "slippage_percent": 0.003
}

print("Starting...")

arbitrum_config_object = ConfigManager(chain='arbitrum')
arbitrum_config_object.set_config()

order_parameters = OrderArgumentParser(
    config=arbitrum_config_object,
    is_increase=False
).process_parameters_dictionary(
    parameters
)

print(f"order_parameters: {order_parameters}")

order = IncreaseOrder(
    config=arbitrum_config_object,
    market_key=order_parameters['market_key'],
    collateral_address=order_parameters['collateral_address'],
    index_token_address=order_parameters['index_token_address'],
    is_long=order_parameters['is_long'],
    size_delta=order_parameters['size_delta'],
    initial_collateral_delta_amount=order_parameters['initial_collateral_delta'],
    slippage_percent=order_parameters['slippage_percent'],
    swap_path=order_parameters['swap_path'],
    debug_mode=True
)
