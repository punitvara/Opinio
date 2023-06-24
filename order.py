import uuid

class Order:
    def __init__(self, user_id, question_id, trade_type:str, quantity:int, side :str, price:float, time_stamp:int):
        self.order_id = self.generate_order_id()  # Implement a method to generate a unique order ID
        self.user_id = user_id
        self.question_id = question_id
        self.trade_type = trade_type
        self.quantity = quantity
        self.side = side
        self.price = price
        self.status = 'pending'
        self.time_stamp = time_stamp

    def generate_order_id(self):
        return uuid.uuid4().hex[:6].upper()
    
    
