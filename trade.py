class Order:
    def __init__(self, user_id) -> None:
        self.user_id = user_id
        self.order_id = 0
        self.status = "Open"