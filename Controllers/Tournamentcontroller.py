from datetime import datetime
from Models.database import *
from operator import attrgetter
from Controllers.Menucontroller import *
from Views.Playerview import PlayerView
from Models.database import Database
from Views.Tournamentview import TournamentView
from Models.Roundmodel import Round


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
        if not self.tournament:
            list_of_ongoing_tournaments = self.database.load_ongoing_tournaments()
            user_choice = self.select_tournament_from_list(list_of_ongoing_tournaments)
            self.tournament = self.database.deserialize_tournament_info(user_choice)
            return self.play_1st_round(self.tournament)
        else:
            self.play_1st_round(self.tournament)

    def select_tournament_from_list(self, list_of_ongoing_tournaments):
        user_choice = self.tournament_view.get_user_touurnament_choice_from_list(list_of_ongoing_tournaments)
        return user_choice

    def play_1st_round(self, tournament):
        self.tournament = tournament
        self.players = self.tournament.tournament_players_ranking
        self.tournament.tournament_players_ranking.sort(key=attrgetter('rank'))
        self.round = Round(self.tournament.actual_round, self.tournament.tournament_players_ranking)
        self.round.pairs = self.round.generate_1st_round_pairs()
        for match in self.round.pairs:
            match = match.get_result(self.tournament_view.get_match_result(match))
            self.tournament.add_elo_to_players_from_match(match)
        self.round.end_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        self.tournament.round_list.append(self.round)
        self.database.save_tournament_in_db(self.tournament.serialize_tournament_info(), self.tournament.tournament_id)
        return self.play_next_rounds(self.tournament)

    def play_next_rounds(self, tournament):
        self.tournament = tournament
        while len(self.tournament.round_list) <= self.tournament.nb_of_rounds:
            self.tournament.actual_round = len(self.tournament.round_list)
            self.database.save_tournament_in_db(self.tournament.serialize_tournament_info(),
                                                self.tournament.tournament_id)
            self.round = Round(self.tournament.actual_round, self.tournament.tournament_players_ranking)
            self.round.go_to_next_round()
            for match in self.round.pairs:
                match = match.get_result(self.tournament_view.get_match_result(match))
                self.tournament.add_elo_to_players_from_match(match)
            self.round.end_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            self.tournament.round_list.append(self.round)
        self.tournament.end_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        self.database.save_tournament_in_db(self.tournament.serialize_tournament_info(),
                                            self.tournament.tournament_id)
        return


class CreateNewTournamentController:
    user_choice = bool

    def __init__(self):
        self.tournament_view = TournamentView()
        self.player_view = PlayerView()
        self.new_tournament: ""
        self.new_players = []
        self.database = Database()

    def __call__(self):
        tournament = self.tournament_view.get_tournament_info()
        self.new_tournament = Tournament(tournament)
        new_tournament_players = self.player_view.get_player_info()
        for player in new_tournament_players:
            player = Player(player)
            serialized_player_info = player.serialize_player_info()
            self.database.save_player_in_db(serialized_player_info, player.id)
            self.new_tournament.tournament_players_ranking.append(player)
        user_choice = self.tournament_view.continue_tournament(tournament)  # Change it so it prints only
        # necessary tournament  info
        serialized_tournament = self.new_tournament.serialize_tournament_info()
        self.database.save_tournament_in_db(serialized_tournament, self.new_tournament.tournament_id)
        if user_choice is True:
            return LiveTournamentController(self.new_tournament)
        else:
            return HomeMenuController()

