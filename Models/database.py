from tinydb import TinyDB, Query
from Models.Playermodel import Player
from Models.Tournamentmodel import Tournament


class Database:
    def __init__(self):
        self.database = TinyDB('db.json')
        self.query = Query()
        self.tournaments_table = self.database.table('Tournament')
        self.players_table = self.database.table('Players')

    def save_tournament_in_db(self, serialized_tournament,  tournament_id):
        """
        :param serialized_tournament:
        :param tournament_id:
        :return:
        """
        self.tournaments_table.upsert(serialized_tournament, self.query.tournament_id == tournament_id)

    @staticmethod
    def deserialize_tournament_info(serialized_tournament):
        list_of_players = []
        tournament = Tournament(serialized_tournament)
        for player in tournament.tournament_players_ranking:
            player = Player(player)
            list_of_players.append(player)
        tournament.tournament_players_ranking = list_of_players
        return tournament

    @staticmethod
    def deserialize_player_info(serialized_player):
        player = Player(serialized_player)
        return player

    def load_players_from_tournament_id(self, tournament_id):
        tournament = self.tournaments_table.search(self.query.tournament_id == tournament_id)
        tournament_players = tournament['tournament_players_ranking']
        return tournament_players

    def load_all_players(self):
        players = self.players_table.all()
        return players

    def load_tournament_from_db(self, tournament_name_or_id=False):
        """
        Load a tournament from db if no arg then load all tournaments
        :param: name or id of the tournament
        :return: tournament info as dict
        """
        if not tournament_name_or_id:
            tournament = self.tournaments_table.all()
            return tournament
        elif len(tournament_name_or_id) < 36:
            tournament = self.tournaments_table.search(self.query.name == tournament_name_or_id)
            print(tournament, 'By name')
            return tournament
        elif len(tournament_name_or_id) > 35:
            tounament = self.tournaments_table.search(self.query.tournament_id == tournament_name_or_id)
            print(tounament, 'by id')
            return tounament

    def load_ongoing_tournaments(self):
        unfinished_tournament = self.tournaments_table.search(self.query.end_date == False)
        return unfinished_tournament

    def save_player_in_db(self, serialized_player, player_id):
        self.players_table.upsert(serialized_player, self.query.id == player_id)
