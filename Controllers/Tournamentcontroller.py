from datetime import datetime
import Controllers
from Views.Playerview import PlayerView
from Models.database import Database
from Views.Tournamentview import TournamentView
from Models.Roundmodel import Round
from Models.Playermodel import Player
from Models.Tournamentmodel import Tournament


class LiveTournamentController:
    list_of_ongoing_tournaments = []

    def __init__(self, tournament_id=False):
        self.tournament_id = tournament_id
        self.tournament = ""
        self.players = []
        self.tournament_view = TournamentView()
        self.database = Database()
        self.round = ""

    def __call__(self):
        """
        if no tournament loaded, loads all ongoing tournaments, load them to the view and returns user's tournament id
         choice to other LiveTournamentController method
         else returns tournament_id to play_tournament
        :return: tournament id
        """
        if not self.tournament_id:
            list_of_ongoing_tournaments = self.database.load_ongoing_tournaments()
            self.tournament_id = self.select_tournament_from_list(
                list_of_ongoing_tournaments
            )
            if self.tournament_id == "0":
                return Controllers.Menucontroller.HomeMenuController()
        return self.play_tournament(self.tournament_id)

    def select_tournament_from_list(self, list_of_ongoing_tournaments):
        """
        Load the list of ongoing tournaments to the view
        :param list_of_ongoing_tournaments: list of tournament with no end date
        :return: users tournament_id choice from list
        """
        user_choice = self.tournament_view.get_user_tournament_choice_from_list(
            list_of_ongoing_tournaments
        )
        if user_choice == "0":
            return user_choice
        self.tournament = self.database.load_tournament_from_id(user_choice)
        return user_choice

    def play_tournament(self, tournament_id):
        """
        Load Tournament object from tournament ID, loops over round_id until it reaches nb_of_round
        :param tournament_id:
        """
        self.tournament = self.database.load_tournament_from_id(tournament_id)
        self.players = self.database.load_players_from_tournament_id(self.tournament_id)
        while self.tournament.round_id < self.tournament.nb_of_rounds:
            self.tournament, self.players = self.play_round()
            if self.tournament and self.players == "0":
                return LiveTournamentController()
        self.tournament.end_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        self.tournament_view.display_end_tournament(self.tournament, self.players)

        self.database.save_tournament_in_db(
            self.tournament.serialize_tournament_info(), self.tournament_id
        )
        return Controllers.Menucontroller.HomeMenuController()

    def play_round(self):
        """
        Play tournament round
        :returns tournament object, list of players object
        """
        if self.tournament.round_id == 0:
            round_info = self.tournament.generate_1st_round_pairs(self.players)
        else:
            round_info = self.tournament.generate_next_round_pairs(self.players)
        match_list, round_start_time = round_info
        self.round = Round(match_list, round_start_time)
        user_input = self.tournament_view.display_tournament_info(
            self.tournament, self.round
        )
        if user_input == "0":
            return "0", "0"
        else:
            for match in self.round.match_list:
                closed_match = self.tournament_view.get_match_result(match)
                (p_1, score_p1), (p_2, score_p2) = closed_match
                for player in self.players:
                    if player.p_id == p_1.p_id:
                        player.add_points(score_p1)
                        player.add_id_to_opponent_list(p_2.p_id)
                        self.database.save_player_in_db(
                            player.serialize_player_info(), player.p_id
                        )
                    elif player.p_id == p_2.p_id:
                        player.add_points(score_p2)
                        player.add_id_to_opponent_list(p_1.p_id)
                        self.database.save_player_in_db(
                            player.serialize_player_info(), player.p_id
                        )
        self.round.end_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        formated_match_list = self.round.format_match_list()
        self.tournament.round_list.append(
            {
                "match_list": formated_match_list,
                "start_time": self.round.start_time,
                "end_time": self.round.end_time,
            }
        )
        self.tournament.round_id += 1
        self.database.save_tournament_in_db(
            self.tournament.serialize_tournament_info(), self.tournament_id
        )
        return self.tournament, self.players


class CreateNewTournamentController:
    user_choice = bool

    def __init__(self):
        self.tournament_view = TournamentView()
        self.player_view = PlayerView()
        self.new_tournament = ""
        self.new_players = []
        self.database = Database()

    def __call__(self):
        """Do function to make it CLEAAAAANEEEEERRR"""
        tournament_info = self.tournament_view.get_tournament_info()
        self.new_players = self.get_players()
        self.new_tournament = self.get_tournament_obj(tournament_info, self.new_players)
        self.database.save_tournament_in_db(
            self.new_tournament.serialize_tournament_info(),
            self.new_tournament.tournament_id,
        )
        user_choice = self.tournament_view.continue_tournament(self.new_tournament)
        if user_choice is True:
            return LiveTournamentController(self.new_tournament.tournament_id)
        else:
            return Controllers.Menucontroller.HomeMenuController()

    def get_players(self):
        players = self.player_view.get_player_info()
        for p in players:
            p = Player(
                first_name=p["first_name"],
                last_name=p["last_name"],
                age=p["age"],
                gender=p["gender"],
                birth_date=p["birth_date"],
                elo=p["elo"],
                tournament_points=p["tournament_points"],
                p_id=p["p_id"],
                opponent=p["opponent"],
            )
            self.database.save_player_in_db(p.serialize_player_info(), p.p_id)
            self.new_players.append(p)
        return self.new_players

    def get_tournament_obj(self, tournament_info, tournament_players):
        players_id = [p.p_id for p in tournament_players]
        self.new_tournament = Tournament(
            name=tournament_info["name"],
            location=tournament_info["location"],
            description=tournament_info["description"],
            nb_of_round=tournament_info["nb_of_round"],
            time_set=tournament_info["time_set"],
            tournament_players_id=players_id,
            tournament_id=tournament_info["tournament_id"],
            round_id=tournament_info["round_id"],
            begin_date=tournament_info["begin_date"],
            end_date=tournament_info["end_date"],
        )
        return self.new_tournament
