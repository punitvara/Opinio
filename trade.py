class Trade:
    def __init__(self, buyer_id, seller_id, question_id, side, quantity, price, timestamp):
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.question_id = question_id
        self.side = side  # 'YES' or 'NO'
        self.quantity = quantity
        self.price = price
        self.timestamp = timestamp
