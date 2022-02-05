from tinydb import TinyDB
from Models.Playermodel import *
from Models.Tournamentmodel import *



class Match:
    def __init__(self, round_id, player1, player2):
        self.round_id = round_id
        self.player1: Player = player1
        self.player2: Player = player2
        self.score = False

    def __repr__(self):
        result = ""
        if not self.score:
            result = "Match pas encore jouer"
        elif self.score == self.player1.last_name:
            result = f"Victoire de {self.player1.last_name}"
        elif self.score == self.player2.last_name:
            result = f"Victoire de {self.player2.last_name}"
        elif self.score == 'Nulle':
            result = f"Partie nulle"
        return (f"{self.player1} vs {self.player2} \n"
                f"Resultat : {result}\n")

    def serialize_match_result(self):
        return {'round_id': self.round_id,
                'player1': self.player1,
                'score_player1': self.score_player1,
                'player2': self.player2,
                'score_player2': self.score_player2}

    def save_match(self):
        db = TinyDB('db.json')
        match_info_table = db.table('Matchs')
        match_info_table.insert(self.serialize_match_result())
        return

    def get_result(self, result):
        self.score = result
        return self