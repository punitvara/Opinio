class Market:
    def __init__(self):
        self.orders = []
        self.trades = []

    def add_order(self, order):
        self.orders.append(order)
        self.match_orders(order)

    def remove_order(self, order):
        self.orders.remove(order)

    def add_trade(self, trade):
        self.trades.append(trade)

    def match_orders(self, new_order):
        matching_orders = []

        for order in self.orders:
            if (
                order.question_id == new_order.question_id
                and order.trade_type != new_order.trade_type
                and order.price == new_order.price
            ):
                matching_orders.append(order)

        for order in matching_orders:
            if order.quantity >= new_order.quantity:
                self.execute_trade(new_order, order)
                self.remove_order(order)
            else:
                self.execute_trade(new_order, order)
                new_order.quantity -= order.quantity
                self.remove_order(order)

    def execute_trade(self, buy_order, sell_order):
        trade_quantity = min(buy_order.quantity, sell_order.quantity)
        trade_price = buy_order.price

        trade = Trade(
            buy_order.user_id,
            sell_order.user_id,
            buy_order.question_id,
            trade_quantity,
            trade_price,
        )
        self.add_trade(trade)

        buy_order.quantity -= trade_quantity
        sell_order.quantity -= trade_quantity

        if buy_order.quantity == 0:
            self.remove_order(buy_order)

        if sell_order.quantity == 0:
            self.remove_order(sell_order)


# class Market:
#     def __init__(self):
#         self.order_book = [] # List of orders # copilot was suggesting dictionary here
#         self.trades = []

#     def add_trade(self, trade):
#         self.trades.append(trade)

#     def get_trades_for_question(self, q_id):
#         return [trade for trade in self.trades if trade.q_id == q_id]

#     def get_trades_for_user(self, user_id):
#         return [trade for trade in self.trades if trade.user_id == user_id]

#     def get_total_quantity_for_question(self, q_id):
#         trades = self.get_trades_for_question(q_id)
#         total_quantity = sum(trade.quantity for trade in trades)
#         return total_quantity

#     def get_price_for_question(self, q_id):
#         trades = self.get_trades_for_question(q_id)
#         if not trades:
#             return 0

#         total_value = sum(trade.quantity * trade.price for trade in trades)
#         total_quantity = self.get_total_quantity_for_question(q_id)
#         average_price = total_value / total_quantity
#         return average_price
