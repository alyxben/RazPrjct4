from tinydb import TinyDB, Query


class Player:
    def __init__(self, first_name, last_name, age, gender, birth_date, elo, tournament_points, opponent, id):
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.age: str = age
        self.gender: str = gender
        self.birth_date: str = birth_date
        self.elo = int(elo)
        self.tournament_points: float = float(tournament_points)
        self.opponent: list = opponent
        self.id: str = id

    def __repr__(self):
        return f"Nom du joueur: {self.last_name}\n" \
               f"Prénom du joueur: {self.first_name}\n" \
               f"Date de naissance: {self.birth_date}\n" \
               f"Nombre de point du joueur: {self.tournament_points}\n" \
               f"Rang du joueur: {self.elo}\n" \
               f"ID: {self.id}\n" \
               f"Opponent: {self.opponent}\n"

    def serialize_player_info(self):
        """
        Serialize the player info so it can be stored in db
        :return: Serialized player info
        """
        return {'first_name': self.first_name,
                'last_name': self.last_name,
                'age': self.age,
                'gender': self.gender,
                'birth_date': self.birth_date,
                'elo': self.elo,
                'tournament_points': self.tournament_points,
                'opponent': self.opponent,
                'id': self.id}

    def add_id_to_opponent_list(self, id):
        self.opponent.append(id)

    def add_points(self, points):
        self.tournament_points += points
