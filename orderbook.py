class OrderBook():
    """
    Fills buy and sell orders
    """
    def __init__(self) -> None:
        # heaps for highest buy and lowest sell prices
        self.best_ask = []
        self.best_bid = []

        # dictionaries for easy retrieval
        self.order_map = {}
        self.volume_map = {}
        self.queue_map = {}