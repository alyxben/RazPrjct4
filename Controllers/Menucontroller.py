from Views.Menuview import HomeMenuView
from Models.Menumodel import MenuModel
from Controllers.Tournamentcontroller import (
    LiveTournamentController,
    CreateNewTournamentController,
)
from Controllers.Rapportcontroller import RapportSubMenu


class AppController:
    """Front Controller"""

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
        """
        Home menu options
        :return: selected controller
        """
        self.menu.add_option("auto", "Continuer un tournoi", LiveTournamentController())
        self.menu.add_option(
            "auto", "Créer un nouveau tournoi", CreateNewTournamentController
        )
        self.menu.add_option("auto", "Rapport", RapportSubMenu())
        user_choice = self.view.get_user_choice()
        return user_choice.handler
