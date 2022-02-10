from tinydb import TinyDB, Query


class Player:
    def __init__(self, player_info):
        self.first_name = player_info["first_name"]
        self.last_name = player_info['last_name']
        self.age = player_info['age']
        self.gender = player_info['gender']
        self.birth_date = player_info['birth_date']
        self.rank = int(player_info['rank'])
        self.elo = int(player_info['elo'])
        self.opponent = []
        self.id = player_info['id']

    def __repr__(self):
        return f"Nom du joueur: {self.last_name}\n" \
               f"Prénom du joueur: {self.first_name}\n" \
               f"Date de naissance: {self.birth_date}\n" \
               f"Elo du joueur: {self.elo}\n" \
               f"Rang du joueur: {self.rank}\n" \
               f"ID: {self.id}\n" \
               f"Opponent: {self.opponent}\n"

    def _serialize_player_info(self):
        """
        Serialize the player info so it can be stored in db
        :return: Serialized player info
        """
        return {'first_name': self.first_name,
                'last_name': self.last_name,
                'age': self.age,
                'gender': self.gender,
                'birth_date': self.birth_date,
                'rank': self.rank,
                'elo': self.elo,
                'opponent': self.opponent,
                'id': self.id}

    def save_player_in_db(self):
        db = TinyDB('db.json')
        player_info_table = db.table('Players')
        player_info_table.insert(self._serialize_player_info())

    def sort_players_by_rank(self, players_list):
        sorted_player_by_rank = sorted(players_list, key=lambda row: row['rank'])
        return sorted_player_by_rank

    def sort_player_by_elo(self, players_list):
        sorted_player_by_elo = sorted(players_list, key=lambda row: row['elo'], reverse=True)
        return sorted_player_by_elo

    def sort_player_by_alphab(self, players_list):
        sorted_player_by_alpha = sorted(players_list, key=lambda row: row['last_name'])
        return sorted_player_by_alpha

    def load_players_from_db(self, players_ids):
        """

        :param players_ids: list of player id's
        :return: list of dict corresponding to players_ids
        """
        db = TinyDB('db.json')
        players_info_table = db.table('Players')
        players_list_updated = []
        for id in players_ids:
            players_list_updated.append(players_info_table.search(Query().id == id)[0])
        return players_list_updated

    def update_player_list(self, tournament_name):
        db = TinyDB('db.json')
        players_info_table = db.table('Tournament')
        players_list = players_info_table.search(Query().name == tournament_name)
        print(players_list)
        return players_list[0]['tournament_players_ranking']
