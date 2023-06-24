class Tournament:
    def __init__(self, tournament_id, name, start_date, end_date):
        self.tournament_id = tournament_id
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.matches = []

    def add_match(self, match):
        self.matches.append(match)
