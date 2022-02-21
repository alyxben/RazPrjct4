from Views.Menuview import HomeMenuView
from Models.Menumodel import MenuModel
from Models.Tournamentmodel import Tournament
from Models.Playermodel import Player
from Views.Tournamentview import TournamentView
from Controllers.Tournamentcontroller import LiveTournamentController, CreateNewTournamentController
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
        self.menu.add('auto', 'Créer un nouveau tournoi', CreateNewTournamentController)
        self.menu.add('auto', 'Continuer un tournoi', LiveTournamentController())
        #self.menu.add('auto', 'Générer un rapport de tournoi', CreateTournamentInfoFile())
        #self.menu.add('auto', 'Générer un rapport de joueur', ManagePlayers())
        #self.menu.add('auto', 'Gérer les joueurs', ManagePlayers())
        #self.menu.add('q', 'Quitter', QuittAppController())

        user_choice = self.view.get_user_choice()

        return user_choice.handler


