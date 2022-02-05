from Models.Matchmodel import Match
from Models.Roundmodel import Round
from Models.Playermodel import Player
from Models.Tournamentmodel import Tournament
from tinydb import TinyDB
from Models.database import *
from Views.Tournamentview import TournamentView
from Views.Menuview import HomeMenuView
from Models.database import Database
from Models.Menumodel import MenuModel
from operator import attrgetter


class LiveTournamentController:
    list_of_ongoing_tournaments = []

    def __init__(self, tournament=''):
        self.tournament = tournament
        self.players = []
        self.menu = MenuModel()
        self.view = TournamentView()
        self.menu_view = HomeMenuView(self.menu)
        self.database = Database()
        self.actual_round = ""
        self.actual_round = []
        self.round_result = []

    def __call__(self):
        if self.tournament == '':
            list_of_ongoing_tournaments = self.database.load_ongoing_tournaments()
            self.select_tournament_from_list(list_of_ongoing_tournaments)

    def select_tournament_from_list(self, list_of_ongoing_tournaments):
        user_choice = self.view.get_user_touurnament_choice_from_list(list_of_ongoing_tournaments)
        return self.play_tournament(user_choice)

    def play_tournament(self, tournament):
        self.tournament = Tournament(tournament)
        for player in self.tournament.tournament_players_ranking:
            self.players.append(Player(player))
        self.players.sort(key=attrgetter('rank'))
        while self.tournament.actual_round <= self.tournament.nb_of_rounds:
            self.tournament.tournament_players_ranking = self.players
            self.actual_round = Round(self.tournament)
            self.actual_round.generate_1st_round_pairs()
            for match in self.actual_round.pairs:
                match = match.get_result(self.view.get_match_result(match))
                self.tournament.add_elo_to_players_from_match(match)
            self.tournament.actual_round += 1
            self.tournament.tournament_players_ranking.sort(key=attrgetter('elo'), reverse=True)
            self.actual_round.generate_next_round_pairs()
            for match in self.actual_round.pairs:
                match = match.get_result(self.view.get_match_result(match))
                self.tournament.add_elo_to_players_from_match(match)
            self.tournament.actual_round += 1


class CreateTournamentInfoFile:
    pass
