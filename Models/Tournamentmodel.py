from datetime import datetime
from tinydb import TinyDB, Query
from .Roundmodel import *
from Models.Matchmodel import *
from .Playermodel import *
from operator import attrgetter


class Tournament:
    def __init__(self, tournament_info):
        self.name = tournament_info['tournament_name']
        self.location = tournament_info['location']
        self.description = tournament_info['description']
        if tournament_info['nb_of_round'] == '':
            self.nb_of_rounds = 4
        else:
            self.nb_of_rounds = int(tournament_info['nb_of_round'])
        self.time_set = tournament_info['time_set']
        self.tournament_players_ranking: list = tournament_info['tournament_players']
        self.tournament_id = tournament_info['tournament_id']
        self.actual_round = 1
        self.round_list = []
        self.begin_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        self.end_date = False

    def __repr__(self):
        return f"Nom du tournoi: {self.name}\n" \
               f"Lieu du tournoi: {self.location}\n" \
               f"Date de début du tournoi: {self.begin_date}\n" \
               f"Nombre de Round: {self.nb_of_rounds}\n" \
               f"Nombre de participant: {len(self.tournament_players_ranking)}\n" \
               f"Type de contrôle du temps: {self.time_set}\n" \
               f"Round actuel: {self.actual_round}\n"

    def serialize_tournament_info(self):
        """
        Serialize the tournament info, so it can be stored in db
        :return: Serialized info
        """
        return {'tournament_name': self.name,
                'location': self.location,
                'description': self.description,
                'tournament_players': self.tournament_players_ranking,
                'begin_date': self.begin_date,
                'nb_of_round': self.nb_of_rounds,
                'actual_round': self.actual_round,
                'time_set': self.time_set,
                'tournament_id': self.tournament_id,
                'end_date': self.end_date}

    def add_elo_to_players_from_match(self, match):
        if match.score == 'Nulle':
            for player in self.tournament_players_ranking:
                if player.id == match.player1.id:
                    player.elo += 0.5
                    player.opponent.append(match.player2.id)
                elif player.id == match.player2.id:
                    player.elo += 0.5
                    player.opponent.append(match.player1.id)
        elif match.score == match.player1.last_name:
            for player in self.tournament_players_ranking:
                if player.id == match.player1.id:
                    player.elo += 1
                    player.opponent.append(match.player2.id)
                elif player.id == match.player2.id:
                    player.opponent.append(match.player1.id)
        elif match.score == match.player2.last_name:
            for player in self.tournament_players_ranking:
                if player.id == match.player2.id:
                    player.elo += 1
                    player.opponent.append(match.player1.id)
                elif player.id == match.player1.id:
                    player.opponent.append(match.player2.id)
        return self
