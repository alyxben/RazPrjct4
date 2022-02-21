from datetime import datetime
from Models.Playermodel import *
from Models.Matchmodel import Match
from operator import attrgetter


class Round:
    def __init__(self, round_id, players_list):
        self.players = players_list
        self.round_id = round_id
        self.match = ""
        self.start_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        self.end_time = ""
        self.pairs = []

    def __repr__(self):
        return f"Round: {self.round_id}\n" \
               f"A débuté le: {self.start_time}\n" \
               f"Les duels pour ce round sont: {self.pairs}\n"

    def generate_1st_round_pairs(self):
        """
        Generates the 1st round pairs
        :return: list of pairs for the 1st round
        """
        i = 0
        middle = len(self.players) // 2
        groups = self.players[:middle], self.players[middle:]
        match_list = []
        while i < middle:
            self.match = Match(self.round_id, player1=groups[0][i], player2=groups[1][i])
            match_list.append(self.match)
            i += 1
        return match_list

    def generate_next_round_pairs(self):
        """
        Associez le joueur 1 avec le joueur 2, le joueur 3 avec le joueur 4, et ainsi de suite.
        Si le joueur 1 a déjà joué contre le joueur 2, associez-le plutôt au joueur 3.
        """
        groups = self.players[::2], self.players[1::2]
        matches = list(zip(groups[0], groups[1]))
        match_list = []
        availables = sorted(self.players, key=attrgetter('elo'))

        for item in range(len(matches)):
            (player_1, player_2) = matches[item]
            availables.remove(player_1)

            if player_2 in player_1.opponent:
                possibles = [p for p in availables if p not in player_1.opponent]

                if not possibles:
                    availables.remove(player_2)
                else:
                    figther = next(iter(sorted(possibles)))
                    matches[item] = (player_1, figther)
                    availables.remove(figther)
                    groups2 = availables[::2], availables[1::2]
                    matches2 = list(zip(groups2[0], groups2[1]))
                    matches[item + 1:] = matches2

        for i in matches:
            match_list.append(Match(round_id=self.round_id, player1=i[0], player2=i[1]))
        return match_list

    def go_to_next_round(self):
        self.round_id += 1
        self.pairs = self.generate_next_round_pairs()
        self.start_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        return self
