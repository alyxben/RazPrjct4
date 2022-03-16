import Controllers
from Models.Menumodel import MenuModel
from Views.Menuview import HomeMenuView
from Models.database import Database
from Views.Rapportview import RapportView


class RapportSubMenu:
    def __init__(self):
        self.menu = MenuModel()
        self.menu_view = HomeMenuView(self.menu)
        self.database = Database()
        self.rapport_view = RapportView()

    def __call__(self):
        """
        Rapport option submenu
        :return:
        """
        self.menu.add_option("auto", "Liste des joueurs", PlayerRapport())
        self.menu.add_option("auto", "Liste des tournois clôturés", TournamentRapport())
        self.menu.add_option(
            "0",
            "Retour au menu principal",
            Controllers.Menucontroller.HomeMenuController(),
        )
        user_choice = self.menu_view.get_user_choice()
        return user_choice.handler


class PlayerRapport:
    """Player rapport handler"""

    def __init__(self):
        self.database = Database()
        self.view = RapportView()
        self.players = []

    def __call__(self):
        """
        Player rapport submenu
        :return: Rapport sub menu when user wants
        """
        user_choice = self.view.display_players_list(self.database.load_all_players())
        if user_choice == "0":
            return RapportSubMenu()


class TournamentRapport:
    """Tournament rapport handler"""

    def __init__(self):
        self.database = Database()
        self.view = RapportView()
        self.tournaments = self.database.load_closed_tournaments()

    def __call__(self):
        """
        Tournament rapport submenu, controlls the display of tournament info with user input
        :return: Rapport sub menu when user wants
        """
        user_choices = self.view.get_user_tournament_choice_from_list(self.tournaments)
        if user_choices[1] == "J":
            self.get_tournament_players(user_choices[0])
        elif user_choices[1] == "R":
            self.get_tournament_rounds(user_choices[0])
        elif user_choices[1] == "M":
            self.get_tournament_matchs(user_choices[0])
        elif user_choices[1] == "0":
            return RapportSubMenu()

    def get_tournament_players(self, tournament):
        """
        Loads tournament players list and load it to the view
        :param tournament: Tournament object
        """
        players_id = tournament.tournament_players_id
        players_list = []
        for p_id in players_id:
            players_list.append(self.database.load_player_from_id(p_id))
        user_choice = self.view.display_players_list(players_list)
        if user_choice == "0":
            return RapportSubMenu()

    def get_tournament_rounds(self, tournament):
        """
        Load tournament round list and load it to the view
        :param tournament: Tournament object
        :return:
        """
        deserialized_round = []
        for r in tournament.round_list:
            deserialized_round.append(self.database.deserialize_round_info(r))
        self.view.display_round_list(deserialized_round)

    def get_tournament_matchs(self, tournament):
        """
        Load all the matchs and load them to the view
        :param tournament:
        :return:
        """
        match_list = []
        for r in tournament.round_list:
            matchs = r["match_list"]
            for m in matchs:
                match_list.append(m)
        self.view.display_matchs(match_list)
