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

    def save_tournament_in_db(self, serialized_tournament,  tournament_id):
        self.tournaments_table.upsert(serialized_tournament, self.query.id == tournament_id)

    def load_tournament_from_db(self, tournament_name_or_id=False):
        """
        Load a tournament from db
        :param tournament_id: tournament id to search
        :param tournament_name: name of the tournament to searh
        :return: tournament info
        """
        if not tournament_name_or_id:
            return False
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
