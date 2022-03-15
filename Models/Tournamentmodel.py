from .Roundmodel import *
from operator import attrgetter


class Tournament:
    def __init__(self, name, location, description, nb_of_round, time_set, tournament_players_id, tournament_id,
                 round_id, begin_date, round_list=[], end_date=False):
        self.name: str = name
        self.location: str = location
        self.description: str = description
        if nb_of_round == '':
            self.nb_of_rounds: int = 4
        else:
            self.nb_of_rounds: int = int(nb_of_round)
        self.time_set: str = time_set
        self.tournament_players_id: list = tournament_players_id
        self.tournament_id: str = tournament_id
        self.round_id: int = int(round_id)
        self.round_list: list = round_list
        self.begin_date: str = begin_date
        self.end_date: str = end_date

    def __repr__(self):
        if self.end_date is not False:
            return f"Nom du tournoi: {self.name}\n" \
                   f"Lieu du tournoi: {self.location}\n" \
                   f"Date de début du tournoi: {self.begin_date}\n" \
                   f"Le tournoi a été joué en {self.nb_of_rounds} round\n" \
                   f"Date de fin du tournoi: {self.end_date}"
        else:
            return f"Nom du tournoi: {self.name}\n" \
                   f"Lieu du tournoi: {self.location}\n" \
                   f"Date de début du tournoi: {self.begin_date}\n" \
                   f"Nombre de Round: {self.nb_of_rounds}\n" \
                   f"Nombre de participant: {len(self.tournament_players_id)}\n" \
                   f"Type de contrôle du temps: {self.time_set}\n" \
                   f"Round actuel: {self.round_id}\n"

    def serialize_tournament_info(self):
        return {'name': self.name,
                'location': self.location,
                'description': self.description,
                'tournament_players_id': self.tournament_players_id,
                'begin_date': self.begin_date,
                'nb_of_round': self.nb_of_rounds,
                'round_id': self.round_id,
                'round_list': self.round_list,
                'time_set': self.time_set,
                'tournament_id': self.tournament_id,
                'end_date': self.end_date}

    def generate_1st_round_pairs(self, tournament_players):
        """
        Generates the 1st round pairs, according to the swiss pairing system
        :return: list of pairs for the 1st round
        """
        self.begin_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        round_start_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        tournament_players = sorted(tournament_players, key=attrgetter('elo'))
        i = 0
        middle = len(tournament_players) // 2
        groups = tournament_players[:middle], tournament_players[middle:]
        match_list = []
        while i < middle:
            match = ([groups[0][i]], [groups[1][i]])
            match_list.append(match)
            i += 1
        return match_list, round_start_time

    def generate_next_round_pairs(self, tournament_players):
        """
        Sort tournament players list by points and pairs them according to Swiss pairing system
        :param tournament_players: tournament players list
        :return: Tuple containing match for the round, round start time
        """
        tournament_players.sort(key=attrgetter('tournament_points'), reverse=True)
        groups = tournament_players[::2], tournament_players[1::2]
        matchs = list(zip(groups[0], groups[1]))
        availables = sorted(tournament_players, key=attrgetter('tournament_points'), reverse=True)
        match_list = []
        round_start_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        for item in range(len(matchs)):
            (player_1, player_2) = matchs[item]
            availables.remove(player_1)

            if player_2.id in player_1.opponent:
                possibles = [p for p in availables if p.id not in player_1.opponent]

                if not possibles:
                    availables.remove(player_2)
                else:
                    fighter = next(iter(possibles))
                    matchs[item] = (player_1, fighter)
                    availables.remove(fighter)
                    groups2 = availables[::2], availables[1::2]
                    matches2 = list(zip(groups2[0], groups2[1]))
                    matchs[item + 1:] = matches2
            else:
                availables.remove(player_2)
        for i in matchs:
            p1 = i[0]
            p2 = i[1]
            pair = ([p1], [p2])
            match_list.append(pair)
        return match_list, round_start_time
