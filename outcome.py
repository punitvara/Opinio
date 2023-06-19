class Outcome:
    def __init__(self, q_id : int) -> None:
        self.q_id = q_id
        self.prob_yes = 0
        self.prob_no  = 0
        self.prob_draw = 0
        self.price_yes = 0
        self.price_no = 0
        self.price_draw = 0
        
    def set_price_yes(self, price: float) -> None:
        self.price_yes = price

    def set_price_no(self, price: float) -> None:
        self.price_no = price
    
    def get_price_yes(self) -> float:
        return self.price_yes

    def get_price_no(self) -> float:
        return self.price_no 
        
    def refresh(self):
        pass
        
        # self.user = User()
        # self.sot = SourceOfTruth()
        # self.question = Question()
        # self.wallet = Wallet()
        # self.order = Order()
        # self.bet = Bet()
        # self.bet_result = BetResult()