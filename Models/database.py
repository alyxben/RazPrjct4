from tinydb import TinyDB, Query
from Models.Playermodel import Player
from Models.Tournamentmodel import Tournament
from Models.Roundmodel import Round


class Database:
    def __init__(self):
        self.database = TinyDB('db.json')
        self.query = Query()
        self.tournaments_table = self.database.table('Tournament')
        self.players_table = self.database.table('Players')

    def save_tournament_in_db(self, serialized_tournament, tournament_id):
        """
        :param serialized_tournament: serialized tournament info
        :param tournament_id: tournament id
        """
        self.tournaments_table.upsert(serialized_tournament, self.query.tournament_id == tournament_id)

    def save_player_in_db(self, serialized_player, player_id):
        self.players_table.upsert(serialized_player, self.query.id == player_id)

    def load_player_from_id(self, player_id):
        """
                Load player from db with id
        :param player_id: player id
        :return: Player object
        """
        player = self.players_table.search(self.query.id == player_id)[0]
        player = self.deserialize_player_info(player)
        return player

    def load_players_from_tournament_id(self, tournament_id):
        """
                Get players id from tournament_id and load players
        :param tournament_id: tournament id
        :return: list of Player objects
        """
        tournament_players = []
        tournament = self.tournaments_table.search(self.query.tournament_id == tournament_id)[0]
        tournament_players_id = tournament['tournament_players_id']
        for id in tournament_players_id:
            tournament_players.append(self.load_player_from_id(id))
        return tournament_players

    def load_all_players(self):
        """
                Load all players
        :return: list of Player objects
        """
        players_list = []
        players = self.players_table.all()
        for player in players:
            players_list.append(Player(last_name=player['last_name'], first_name=player['first_name'],
                                       age=player['age'], gender=player['gender'],
                                       birth_date=player['birth_date'],
                                       elo=player['elo'], tournament_points=player['tournament_points'],
                                       id=player['id'],
                                       opponent=player['opponent']))
        return players_list

    def load_tournament_from_id(self, tournament_id):
        """
                Load tournament with tournament id
        :param tournament_id: id of the tournament
        :return: tournament object
        """
        tournament = self.tournaments_table.search(self.query.tournament_id == tournament_id)[0]
        tournament = self.deserialize_tournament_info(tournament)
        return tournament

    def load_ongoing_tournaments(self):
        """
                Load all tournaments with end_date False
        :return: list of Tournament objects
        """
        tournaments_list_deserialized = []
        unfinished_tournament = self.tournaments_table.search(self.query.end_date == False)
        for t in unfinished_tournament:
            tournaments_list_deserialized.append(self.deserialize_tournament_info(t))
        return tournaments_list_deserialized

    def load_closed_tournaments(self):
        """
                Load all tournaments who reached the 4th round
        :return: list of Tournament objects
        """
        tournaments_list_deserialized = []
        closed_tournaments = self.tournaments_table.search(self.query.end_date != False)
        for t in closed_tournaments:
            tournaments_list_deserialized.append(self.deserialize_tournament_info(t))
        return tournaments_list_deserialized

    @staticmethod
    def deserialize_player_info(serialized_player):
        player = Player(last_name=serialized_player['last_name'], first_name=serialized_player['first_name'],
                        age=serialized_player['age'], gender=serialized_player['gender'],
                        birth_date=serialized_player['birth_date'],
                        elo=serialized_player['elo'], tournament_points=serialized_player['tournament_points'],
                        id=serialized_player['id'],
                        opponent=serialized_player['opponent'])
        return player

    @staticmethod
    def deserialize_round_info(serialized_round):
        round = Round(match_list=serialized_round['match_list'], start_time=serialized_round['start_time'],
                      end_time=serialized_round['end_time'])
        return round

    def deserialize_tournament_info(self, serialized_tournament):
        round_list = []
        for r in serialized_tournament['round_list']:
            deserialized_round = self.deserialize_round_info(r)
            round_list.append(deserialized_round)
        tournament = Tournament(name=serialized_tournament['name'], location=serialized_tournament['location'],
                                description=serialized_tournament['description'],
                                nb_of_round=serialized_tournament['nb_of_round'],
                                time_set=serialized_tournament['time_set'],
                                tournament_players_id=serialized_tournament['tournament_players_id'],
                                tournament_id=serialized_tournament['tournament_id'],
                                round_id=serialized_tournament['round_id'],
                                begin_date=serialized_tournament['begin_date'],
                                end_date=serialized_tournament['end_date'],
                                round_list=round_list)
        return tournament

    # def update_player_rank(self, player_id, new_rank):
    #     player = self.players_table.search(self.query.id == player_id)[0]
    #     player = self.deserialize_player_info(player)
    #     play
