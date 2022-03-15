from datetime import datetime
import Controllers
from Models.database import *
from Controllers.Menucontroller import *
from Views.Playerview import PlayerView
from Models.database import Database
from Views.Tournamentview import TournamentView
from Models.Roundmodel import Round
from uuid import uuid1


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
        """
        if no tournament loaded, loads all ongoing tournaments, load them to the view and returns user's tournament id
         choice to other LiveTournamentController method
        :return: tournament id
        """
        if not self.tournament_id:
            list_of_ongoing_tournaments = self.database.load_ongoing_tournaments()
            self.tournament_id = self.select_tournament_from_list(list_of_ongoing_tournaments)
        return self.play_tournament(self.tournament_id)

    def select_tournament_from_list(self, list_of_ongoing_tournaments):
        """
        Load the list of ongoing tournaments to the view
        :param list_of_ongoing_tournaments: list of tournament with no end date
        :return: users tournament choice from list
        """
        user_choice = self.tournament_view.get_user_tournament_choice_from_list(list_of_ongoing_tournaments)
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
            self.play_next_round()
        self.tournament.end_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        self.database.save_tournament_in_db(self.tournament.serialize_tournament_info(),
                                            self.tournament.tournament_id)

    def play_next_round(self):
        """
        Plays next tournament round
        """
        if self.tournament.round_id == 0:
            round_info = self.tournament.generate_1st_round_pairs(self.players)
        else:
            round_info = self.tournament.generate_next_round_pairs(self.players)
        match_list, round_start_time = round_info
        self.round = Round(match_list, round_start_time)
        user_input = self.tournament_view.display_tournament_info(self.tournament, self.round)
        if user_input == '0':
            return Controllers.Menucontroller.HomeMenuController()
        else:
            for match in self.round.match_list:
                closed_match = self.tournament_view.get_match_result(match)
                (p_1, score_p1), (p_2, score_p2) = closed_match
                for player in self.players:
                    if player.id == p_1.id:
                        player.add_points(score_p1)
                        player.add_id_to_opponent_list(p_2.id)
                        self.database.save_player_in_db(player.serialize_player_info(), player.id)
                    elif player.id == p_2.id:
                        player.add_points(score_p2)
                        player.add_id_to_opponent_list(p_1.id)
                        self.database.save_player_in_db(player.serialize_player_info(), player.id)
        self.round.end_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        formated_match_list = self.round.format_match_list()
        self.tournament.round_list.append(
            {
                'match_list': formated_match_list, 'start_time': self.round.start_time
                , 'end_time': self.round.end_time})
        self.tournament.round_id += 1
        self.database.save_tournament_in_db(self.tournament.serialize_tournament_info(), self.tournament_id)


class CreateNewTournamentController:
    user_choice = bool

    def __init__(self):
        self.tournament_view = TournamentView()
        self.player_view = PlayerView()
        self.new_tournament = ""
        self.new_players = []
        self.database = Database()

    def __call__(self):
        """ Do function to make it CLEAAAAANEEEEERRR   """
        # tournament = self.tournament_view.get_tournament_info()
        tournament = {'name': str(uuid1()), 'location': '', 'description': '', 'time_set': 'Blitz', 'nb_of_round': '',
                      'tournament_players_id': [], 'tournament_id': '3f1f2496-5887-4300-ab31-ba431cc7a1ba',
                      'round_id': 0, 'round_list': [], 'begin_date': '', 'end_date': False}
        # self.new_players = self.get_players_info()
        new_tournament_players = [
            {'first_name': 'Pierre', 'last_name': 'LAMOUCHE', 'age': '', 'gender': '$', 'birth_date': '', 'elo': 1,
             'id': 'a74d3a04-ee67-417c-8a49-5438a467fb44', 'tournament_points': 0, 'opponent': []},
            {'first_name': 'Pipa', 'last_name': 'BEY', 'age': '', 'gender': '', 'birth_date': '', 'elo': 2,
             'id': '7431c56c-ca56-473d-abf4-28fe2717b135', 'tournament_points': 0, 'opponent': []},
            {'first_name': 'Jeremy', 'last_name': 'CAROL', 'age': '', 'gender': '', 'birth_date': '', 'elo': 3,
             'id': '2ef31caf-2192-4a19-9a28-9ecae9f565d8', 'tournament_points': 0, 'opponent': []},
            {'first_name': 'Pol', 'last_name': 'NOVO', 'age': '', 'gender': '', 'birth_date': '', 'elo': 4,
             'id': '0dbdda1e-7f8e-4555-8ffe-9cf6c11b075c', 'tournament_points': 0, 'opponent': []},
            {'first_name': 'Alyx', 'last_name': 'BEN', 'age': '', 'gender': '', 'birth_date': '', 'elo': 5,
             'id': '3142cad0-4d65-4ec7-93c2-6865a37e47d8', 'tournament_points': 0, 'opponent': []},
            {'first_name': 'Mathilde', 'last_name': 'LAMUSSE', 'age': '', 'gender': '', 'birth_date': '', 'elo': 6,
             'id': '8fa5c3bf-5b28-4786-9610-08643a09cfb9', 'tournament_points': 0, 'opponent': []},
            {'first_name': 'Hugo', 'last_name': 'DTL', 'age': '', 'gender': '', 'birth_date': '', 'elo': 7,
             'id': '53989d0f-cb44-468d-9dc2-5f0b47f41eae', 'tournament_points': 0, 'opponent': []},
            {'first_name': 'Guy', 'last_name': 'MOFITA', 'age': '', 'gender': '', 'birth_date': '', 'elo': 8,
             'id': '5542b1d5-2133-4cea-8e21-4b318afe58e3', 'tournament_points': 0, 'opponent': []}]
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
                                         round_id=tournament['round_id'], begin_date=tournament['begin_date'],
                                         end_date=tournament['end_date'])
        self.database.save_tournament_in_db(self.new_tournament.serialize_tournament_info(),
                                            self.new_tournament.tournament_id)
        user_choice = self.tournament_view.continue_tournament(self.new_tournament)
        if user_choice is True:
            self.new_tournament.begin_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            return LiveTournamentController(self.new_tournament.tournament_id)
        else:
            return Controllers.Menucontroller.HomeMenuController()

    # def get_players(self):
    #     players = self.player_view.get_player_info()
    #     for p in players:
    #         p = Player(first_name=p['first_name'], last_name=p['last_name'], age=p['age'],
    #                    gender=p['gender'], birth_date=p['birth_date'], elo=p['elo'],
    #                    tournament_points=p['tournament_points'], id=p['id'], opponent=p['opponent'])
    #         self.database.save_player_in_db(p.serialize_player_info(), p.id)
    #         self.new_players.append(p)
    #     return self.new_players
    #
    # def get_tournament_obj(self, tournament_info, tournament_players):
    #     players_id = [p['id'] for p in tournament_players]
    #     self.new_tournament = Tournament(name=tournament_info['name'], location=tournament_info['location'],
    #                                      description=tournament_info['description'],
    #                                      nb_of_round=tournament_info['nb_of_round'],
    #                                      time_set=tournament_info['time_set'], tournament_players_id=players_id,
    #                                      tournament_id=tournament_info['tournament_id'],
    #                                      round_id=tournament_info['round_id'],
    #                                      begin_date=tournament_info['begin_date'],
    #                                      end_date=tournament_info['end_date'])
    #     return self.new_tournament
