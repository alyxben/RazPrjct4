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

    def __init__(self, tournament_id=False):
        self.tournament_id = tournament_id
        self.tournament: Tournament = None
        self.players = []
        self.menu = MenuModel()
        self.tournament_view = TournamentView()
        self.menu_view = HomeMenuView(self.menu)
        self.database = Database()
        self.round = ""

    def __call__(self):
        if not self.tournament_id:
            list_of_ongoing_tournaments = self.database.load_ongoing_tournaments()
            self.tournament_id = self.select_tournament_from_list(list_of_ongoing_tournaments)
            print(self.tournament.actual_round)
            if self.tournament.actual_round < 1:
                return self.play_1st_round(self.tournament_id)
            else:
                return self.play_next_rounds(self.tournament_id)
        else:
            self.play_1st_round(self.tournament_id)

    def select_tournament_from_list(self, list_of_ongoing_tournaments):
        user_choice = self.tournament_view.get_user_tournament_choice_from_list(list_of_ongoing_tournaments)
        self.tournament = self.database.load_tournament_from_id(user_choice)
        return user_choice

    def play_1st_round(self, tournament_id):
        self.tournament = self.database.load_tournament_from_id(tournament_id)
        self.players = self.database.load_players_from_tournament_id(self.tournament.tournament_id)
        round_info = self.tournament.generate_1st_round_pairs(self.players)
        self.round = Round(match_list=round_info[0],
                           start_time=round_info[1])
        for match in self.round.match_list:
            match = self.tournament_view.get_match_result(match)
            p_1 = match[0][0]
            p_2 = match[1][0]
            score_p1 = match[0][1]
            score_p2 = match[1][1]
            for player in self.players:
                if player.id == p_1.id:
                    player.add_points(score_p1)
                    player.add_id_to_opponent_list(p_2.id)
                    self.database.save_player_in_db(player.serialize_player_info(), player.id)
                elif player.id == p_2.id:
                    player.add_points(score_p2)
                    player.add_id_to_opponent_list(p_1.id)
                    self.database.save_player_in_db(player.serialize_player_info(), player.id)
        self.tournament.round_list.append(self.round.serialize_round_info())
        self.database.save_tournament_in_db(self.tournament.serialize_tournament_info(), self.tournament_id)
        return self.play_next_rounds(self.tournament_id)

    def play_next_rounds(self, tournament_id):
        self.tournament = self.database.load_tournament_from_id(tournament_id)
        self.players = self.database.load_players_from_tournament_id(self.tournament_id)
        while self.tournament.actual_round < self.tournament.nb_of_rounds:
            round_info = self.tournament.generate_next_round_pairs(self.players)
            match_list = round_info[0]
            round_start_time = round_info[1]
            self.round = Round(match_list, round_start_time)
            print(sorted(self.players, key=attrgetter('tournament_points'), reverse=True))
            for match in self.round.match_list:
                match = self.tournament_view.get_match_result(match)
                p_1 = match[0][0]
                p_2 = match[1][0]
                score_p1 = match[0][1]
                score_p2 = match[1][1]
                for player in self.players:
                    if player.id == p_1.id:
                        player.add_points(score_p1)
                        player.add_id_to_opponent_list(p_2.id)
                        self.database.save_player_in_db(player.serialize_player_info(), player.id)
                    elif player.id == p_2.id:
                        player.add_points(score_p2)
                        player.add_id_to_opponent_list(p_1.id)
                        self.database.save_player_in_db(player.serialize_player_info(), player.id)
            self.tournament.round_list.append(self.round.serialize_round_info())
            self.database.save_tournament_in_db(self.tournament.serialize_tournament_info(),
                                                self.tournament.tournament_id)
        self.tournament.end_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        self.database.save_tournament_in_db(self.tournament.serialize_tournament_info(), self.tournament.tournament_id)
        print(sorted(self.players, key=attrgetter('tournament_points'), reverse=True))
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
        new_tournament_players = self.player_view.get_player_info()
        players_id = [p['id'] for p in new_tournament_players]

        for player in new_tournament_players:
            player = Player(first_name=player['first_name'], last_name=player['last_name'], age=player['age'],
                            gender=player['gender'], birth_date=player['birth_date'], elo=player['elo'],
                            tournament_points=player['tournament_points'], id=player['id'], opponent=player['opponent'])
            self.database.save_player_in_db(player.serialize_player_info(), player.id)
            self.new_players.append(player)

        self.new_tournament = Tournament(name=tournament['name'], location=tournament['location'],
                                         description=tournament['description'], nb_of_round=tournament['nb_of_round'],
                                         time_set=tournament['time_set'], tournament_players_id=players_id,
                                         tournament_id=tournament['tournament_id'],
                                         actual_round=tournament['actual_round'], begin_date=tournament['begin_date'],
                                         end_date=tournament['end_date'])
        print(self.new_tournament)
        self.database.save_tournament_in_db(self.new_tournament.serialize_tournament_info(),
                                            self.new_tournament.tournament_id)
        user_choice = self.tournament_view.continue_tournament(self.new_tournament)
        if user_choice is True:
            self.new_tournament.begin_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            return LiveTournamentController(self.new_tournament.tournament_id)
        else:
            return HomeMenuController()
