from team import Team

class Match:
    def __init__(self, match_id, team1: Team, team2: Team, match_date, venue):
        self.match_id = match_id
        self.team1 = team1
        self.team2 = team2
        self.match_date = match_date
        self.venue = venue
        self.questions = {} # qid: question