from Views.Menuview import HomeMenuView
from Models.Menumodel import MenuModel
from Models.Tournamentmodel import Tournament
from Models.Playermodel import Player
from Views.Tournamentview import TournamentView
from Controllers.Tournamentcontroller import LiveTournamentController
from Controllers.Playercontroller import ManagePlayers



class AppController:
    """ Front Controller """

    def __init__(self):
        self.controller = None

    def start(self):
        """
        runs the app while controller is true
        :return:
        """
        self.controller = HomeMenuController()
        while self.controller:
            self.controller = self.controller()


class HomeMenuController:
    def __init__(self):
        self.menu = MenuModel()
        self.view = HomeMenuView(self.menu)

    def __call__(self):
        self.menu.add('auto', 'Créer un nouveau tournoi', CreateNewTournamentController())
        self.menu.add('auto', 'Continuer un tournoi', LiveTournamentController())
        #self.menu.add('auto', 'Générer un rapport de tournoi', CreateTournamentInfoFile())
        #self.menu.add('auto', 'Générer un rapport de joueur', ManagePlayers())
        #self.menu.add('auto', 'Gérer les joueurs', ManagePlayers())
        #self.menu.add('q', 'Quitter', QuittAppController())

        user_choice = self.view.get_user_choice()

        return user_choice.handler


class CreateNewTournamentController:

    user_choice = bool

    def __init__(self):
        self.view = TournamentView()

    def __call__(self):
        tournament_info = self.view.get_tournament_info()
        tournament_players = self.view.get_player_info()
        new_tournament = self.create_new_tournament(tournament_info)
        players = []
        for player in tournament_players:
            new_tournament.tournament_players_ranking.append(player)
            players.append(self.create_new_player(player))
        new_tournament.save_tournament()
        user_choice = self.view.continue_tournament(new_tournament.name)
        if user_choice is True:
            return LiveTournamentController(new_tournament, players)
        else:
            return HomeMenuController()

    def verify_tournament_info(self, tournament_info):
        for key, value in tournament_info.items():
            if key == 'nb_of_rounds':
                value = int(value)
            else:
                return tournament_info

    def create_new_player(self, player_info):
        new_player = Player(player_info)
        new_player.save_player_in_db()
        return new_player


    def create_new_tournament(self, tournament_info):
        new_tournament = Tournament(tournament_info)
        return new_tournament
        # self.new_tournament.create_new_tournament(tournament_info, tournament_players)
        # self.new_tournament.serialize_tournament_info()
        # self.new_tournament.save_tournament()
        # for player in tournament_players:
        #     self.tournament_player.add_new_player(player)
        #     self.tournament_player.serialize_player_info()
        #     self.tournament_player.save_player_in_db()
        # user_choice = self.view.continue_tournament()
        # if user_choice is True:
        #     return LiveTournamentController(tournament_id=tournament_info['id'])
        # else:
        #     return HomeMenuController()