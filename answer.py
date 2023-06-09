class Answer:
    def __init__(self, q_id : int) -> None:
        self.q_id = q_id
        self.prob_yes = 0
        self.prob_no  = 0
        self.prob_draw = 0
        self.price_yes = 0
        self.price_no = 0
        self.price_draw = 0
        
    
    def refresh(self):
        pass
        
        # self.user = User()
        # self.sot = SourceOfTruth()
        # self.question = Question()
        # self.wallet = Wallet()
        # self.order = Order()
        # self.bet = Bet()
        # self.bet_result = BetResult()