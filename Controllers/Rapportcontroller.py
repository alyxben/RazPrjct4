from Models.Menumodel import MenuModel
from Views.Menuview import HomeMenuView
from Models.database import Database
from Views.Rapportview import RapportView
from Models.Playermodel import Player
from Models.Tournamentmodel import Tournament


class RapportSubMenu:
    def __init__(self):
        self.menu = MenuModel()
        self.menu_view = HomeMenuView(self.menu)
        self.database = Database()
        self.rapport_view = RapportView()

    def __call__(self):
        self.menu.add('auto', 'Liste des joueurs', PlayerRapport())
        self.menu.add('auto', 'Liste des tournois clôturés', TournamentRapport())
        #self.menu.add('auto', "Liste des joueurs d'un tournoi", ) display closed tournament, let user select wich tournament
        #self.menu.add('auto', "Liste des tours d'un tournoi") display closed tournament, let user select wich tournament
        #self.menu.add('auto', "Liste des matchs d'un tournoi") display closed tournament, let user select wich tournament
        user_choice = self.menu_view.get_user_choice()
        return user_choice.handler


class PlayerRapport:
    def __init__(self):
        self.database = Database()
        self.view = RapportView()
        self.players = []

    def __call__(self):
        self.players = self.database.load_all_players()
        self.view.display_players_list(self.players)


class TournamentRapport:
    def __init__(self):
        self.database = Database()
        self.view = RapportView()
        self.tournaments = self.database.load_closed_tournaments()

    def __call__(self):
        user_choices = self.view.get_user_tournament_choice_from_list(self.tournaments)
        if user_choices[1] == 'J':
            self.get_tournament_players(user_choices[0])
        elif user_choices[1] == 'R':
            self.get_tournament_rounds(user_choices[0])
        elif user_choices[1] == 'M':
            self.get_tournament_matchs(user_choices[0])


    def get_tournament_players(self, tournament):
        players_id = tournament.tournament_players_id
        players_list = []
        for id in players_id:
            players_list.append(self.database.load_player_from_id(id))
        self.view.display_players_list(players_list)

    def get_tournament_rounds(self, tournament):
        self.view.display_round_list(tournament.round_list)


    def get_tournament_matchs(self, tournament):
        match_list = []
        for r in tournament.round_list:
            matchs = r['match_list']
            for m in matchs:
                match_list.append(m)
        self.view.display_matchs(match_list)