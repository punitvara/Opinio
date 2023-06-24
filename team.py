class Team:
    def __init__(self, team_id, name):
        self.team_id = team_id
        self.name = name
        self.players = []

    def add_player(self, player):
        self.players.append(player)
