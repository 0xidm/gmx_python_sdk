from . import Order
from ..utils.gas import get_gas_limits
from ..utils import get_datastore_contract


class LimitIncreaseOrder(Order):
    def __init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class LimitDecreaseOrder(Order):
    def __init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class StopLoss(Order):
    def __init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class TakeProfit(Order):
    def __init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
