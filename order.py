from enum import Enum
from datetime import datetime

class Action(Enum):
    """
    Buy or sell action
    """
    BUY = 1
    SELL = 2

class Order():
    """
    Buy or sell order with a timestamp, price, and volume
    """
    def __init__(self, order_id: int, action: Action, price: int, volume: int) -> None:
        self.order_id = order_id
        self.action = action
        self.timestamp = datetime.now()
        self.price = price
        self.volume = volume

