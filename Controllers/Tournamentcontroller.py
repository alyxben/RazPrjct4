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


class LiveTournamentController:
    list_of_ongoing_tournaments = []

    def __init__(self, tournament=False):
        self.tournament = tournament
        self.players = []
        self.menu = MenuModel()
        self.tournament_view = TournamentView()
        self.menu_view = HomeMenuView(self.menu)
        self.database = Database()
        self.actual_round = ""
        self.home_menu = HomeMenuController()


    def __call__(self):
        if not self.tournament:
            list_of_ongoing_tournaments = self.database.load_ongoing_tournaments()
            user_choice = self.select_tournament_from_list(list_of_ongoing_tournaments)
            if user_choice == "0":
                return HomeMenuController()
            else:
                return self.play_tournament(user_choice)

        else:
            self.play_tournament(self.tournament)

    def select_tournament_from_list(self, list_of_ongoing_tournaments):
        user_choice = self.tournament_view.get_user_touurnament_choice_from_list(list_of_ongoing_tournaments)
        return user_choice

    def play_tournament(self, tournament):
        if type(tournament) is not Tournament:
            self.tournament = Tournament(tournament)
        for player in self.tournament.tournament_players_ranking:
            self.players.append(Player(player))
        self.players.sort(key=attrgetter('rank'))
        while self.tournament.actual_round <= self.tournament.nb_of_rounds:
            self.tournament.tournament_players_ranking = self.players
            self.actual_round = Round(self.tournament)
            print(f"       ROUND     {self.actual_round}")
            self.actual_round.generate_1st_round_pairs()
            print(f"{self.actual_round.pairs}, CONTROLLER PRINT")
            for match in self.actual_round.pairs:
                match = match.get_result(self.tournament_view.get_match_result(match))
                self.tournament.add_elo_to_players_from_match(match)
            self.tournament.actual_round += 1
            print(self.tournament.round_list)
            print(f"       ROUND     {self.actual_round}")
            self.tournament.tournament_players_ranking.sort(key=attrgetter('elo'), reverse=True)
            self.actual_round.pairs.clear()
            self.actual_round.generate_next_round_pairs()
            print(f"{self.actual_round.pairs}, CONTROLLER PRINT")
            for match in self.actual_round.pairs:
                match = match.get_result(self.tournament_view.get_match_result(match))
                self.tournament.add_elo_to_players_from_match(match)
            self.tournament.actual_round += 1
        return self.tournament.tournament_players_ranking.sort(key=attrgetter('elo'), reverse=True)


class CreateNewTournamentController:
    user_choice = bool

    def __init__(self):
        self.tournament_view = TournamentView()
        self.player_view = PlayerView()
        self.new_tournament: Tournament = ""
        self.new_players = []
        self.home_menu = HomeMenuController()

    def __call__(self):
        self.new_tournament = Tournament(self.tournament_view.get_tournament_info())
        self.new_players = self.player_view.get_player_info()
        for player in self.new_players:
            player = Player(player)
            player.save_player_in_db()
        self.new_tournament.tournament_players_ranking = self.new_players
        self.new_tournament.save_tournament()
        user_choice = self.tournament_view.continue_tournament(self.new_tournament)
        if user_choice is True:
            return LiveTournamentController(self.new_tournament)
        else:
            return HomeMenuController()

    def verify_tournament_info(self, tournament_info):
        for key, value in tournament_info.items():
            if key == 'nb_of_rounds':
                value = int(value)
            else:
                return tournament_info

    def create_new_player(self, player_info):
        new_player = Player(player_info)
        new_player.save_player_in_db()
        return new_player

    def create_new_tournament(self, tournament_info):
        new_tournament = Tournament(tournament_info)
        return new_tournament


class CreateTournamentInfoFile:
    pass
