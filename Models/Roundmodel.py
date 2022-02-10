from datetime import datetime
from Models.Tournamentmodel import *
from Models.Playermodel import *
from Models.Matchmodel import Match


class Round:
    def __init__(self, tournament):
        self.tournament = tournament
        self.players = self.tournament.tournament_players_ranking
        self.round_id = int(self.tournament.actual_round)
        self.match = ""
        self.start_time = ""
        self.end_time = ""
        self.pairs = []

    def __repr__(self):
        return f"Nom du tournoi: {self.tournament.name}\n" \
               f"Round: {self.round_id}\n" \
               f"A débuté le: {self.start_time}\n" \
               f"Les duels pour ce round sont: {self.pairs}\n"

    def generate_1st_round_pairs(self):
        """
        Generates the 1st round pairs, and saves actual date and time
        :param players_list: list of players sorted by rank
        :return: list of pairs for the 1st round
        """
        self.round_id += 1
        i = 0
        middle = len(self.players) // 2
        groups = self.players[:middle], self.players[middle:]
        while i < middle:
            self.match = Match(self.round_id, player1=groups[0][i], player2=groups[1][i])
            self.pairs.append(self.match)
            i += 1
        return self

    def generate_next_round_pairs(self):
        """

        :param
        :return:
        """
        self.round_id += 1
        middle = len(self.players) // 2
        groups = self.players[:middle], self.players[middle:]
        i = 0
        n = 1
        test_if_already_paired = iter(groups[1])
        while n < middle:
            var = next(test_if_already_paired)
            test = self._check_if_pairable(groups[0][i], var)
            if test is False:
                print(f"{test} LA PAIRE A ETE FAITE")
                self.match = Match(self.round_id, player1=groups[0][i], player2=var)
                self.pairs.append(self.match)
                groups[0].pop(i)
                if len(self.pairs) == middle:
                    return self
                else:
                    n += 1
                    continue
            else:
                print(f"{test} LA PAIRE N'A PAS ETE FAITE")

    def _check_if_pairable(self, player1, player2):
        if player1.id == player2.id or player2.id in player1.opponent:
            return True
        else:
            return False
