from datetime import datetime
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
from Controllers.Menucontroller import *
from Views.Playerview import PlayerView
from Models.database import Database


class LiveTournamentController:
    list_of_ongoing_tournaments = []

    def __init__(self, tournament=False):
        self.tournament = tournament
        self.players = []
        self.menu = MenuModel()
        self.tournament_view = TournamentView()
        self.menu_view = HomeMenuView(self.menu)
        self.database = Database()
        self.round = ""

    def __call__(self):
        if not self.tournament :
            list_of_ongoing_tournaments = self.database.load_ongoing_tournaments()
            user_choice = self.select_tournament_from_list(list_of_ongoing_tournaments)
            return self.play_tournament(user_choice)
        else:
            self.play_tournament(self.tournament)

    def select_tournament_from_list(self, list_of_ongoing_tournaments):
        user_choice = self.tournament_view.get_user_touurnament_choice_from_list(list_of_ongoing_tournaments)
        return user_choice

    def play_tournament(self, tournament):
        self.tournament = Tournament(tournament)
        for player in self.tournament.tournament_players_ranking:
            player = Player(player)
            self.players.append(player)
        self.tournament.tournament_players_ranking = self.players
        self.tournament.tournament_players_ranking.sort(key=attrgetter('rank'))
        self.round = Round(self.tournament.actual_round, self.tournament.tournament_players_ranking)
        self.round.pairs = self.round.generate_1st_round_pairs()
        for match in self.round.pairs:
            match = match.get_result(self.tournament_view.get_match_result(match))
            self.tournament.add_elo_to_players_from_match(match)
        self.round.end_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        self.tournament.round_list.append(self.round)
        while self.tournament.actual_round <= self.tournament.nb_of_rounds:
            self.round.go_to_next_round()
            print(f"CNTROLLEUR {self.round.pairs}")
            for match in self.round.pairs:
                match = match.get_result(self.tournament_view.get_match_result(match))
                self.tournament.add_elo_to_players_from_match(match)
            self.round.end_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            self.tournament.round_list.append(self.round)
            return


class CreateNewTournamentController:
    user_choice = bool

    def __init__(self):
        self.tournament_view = TournamentView()
        self.player_view = PlayerView()
        self.new_tournament_info: ""
        self.new_players = []
        self.database = Database()

    def __call__(self):
        self.new_tournament_info = self.tournament_view.get_tournament_info()
        self.new_players = self.player_view.get_player_info()
        self.new_tournament_info['tournament_players'] = self.new_players
        tournament = Tournament(self.new_tournament_info)
        user_choice = self.tournament_view.continue_tournament(tournament)
        self.database.save_tournament_in_db(tournament.serialize_tournament_info(), tournament.tournament_id)
        if user_choice is True:
            return LiveTournamentController(self.new_tournament_info)
        else:
            return HomeMenuController()



