from order import Action, Order
from collections import deque

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

    def cancel_order(self, order: Order) -> None:
        """
        Removes order (and potentially queue) from associated heap
        """
        if order.order_id in self.order_map:
            # remove order from queue
            order = self.order_map[order.order_id]
            price_queue = self.queue_map[(order.price, order.action)]
            price_queue.remove(order)

            # if queue is empty, remove from heap
            if not price_queue:
                same_book = self.best_bid if order.action == Action.BUY else self.best_ask
                same_book.remove(price_queue)

            # update dictionaries
            self.volume_map[(order.price, order.action)] -= order.volume
            self.order_map.pop(order.order_id)


    def add_order_to_book(self, order: Order) -> None:
        """
        Updates book's orders and volumes, initializing if does not exist
        """
        # price and action does not exist, initialize in dictionaries
        if not (order.price, order.action) in self.queue_map:
            self.queue_map[(order.price, order.action)] = deque([order])
            self.volume_map = [(order.price, order.action)] = order.volume
        else:
            self.queue_map[(order.price, order.action)].append(order)
            self.volume_map[(order.price, order.action)] += order.volume


    def place_order(self, order: Order) -> None:
        """
        Fills a buy or sell order by matching with opposite order(s)
        """
        opposite_book = self.best_ask if order.action == Action.BUY else self.best_bid
        same_book = self.best_bid if order.action == Action.BUY else self.best_ask
        self.order_map[order.order_id] = order

        while order.volume > 0 and opposite_book and opposite_book[0][0].price <= order.price:
            # get price and volume based on matched order
            matched_order = opposite_book[0][0]
            trade_price = matched_order.price
            trade_volume = min(order.volume, matched_order.volume)

            # fill order and remove volume from both buy and sell side
            order.volume -= trade_volume
            matched_order.volume -= trade_volume

            if order.action == Action.BUY:
                print(f"Buy order filled, {trade_volume} shares at {trade_price}.")
            else:
                print(f"Sell order filled, {trade_volume} shares at {trade_price}.")

            if not matched_order.volume:
                self.cancel_order(matched_order)

        if order.volume > 0:
            self.add_order_to_book(order)


    def get_volume_at_price(self, price: int, action: Action):
        """
        Returns the volume at a price and action if it exists
        """
        if (price, action) in self.volume_map:
            return self.volume_map[(price, action)]
        else:
            return 0