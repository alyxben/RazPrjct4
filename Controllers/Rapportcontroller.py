from Models.Menumodel import MenuModel
from Views.Menuview import HomeMenuView
from Models.database import Database


class RapportSubMenu:
    def __init__(self):
        self.menu = MenuModel()
        self.menu_view = HomeMenuView(self.menu)
        self.database = Database()

    def __call__(self):
        self.menu.add('auto', 'Liste des joueurs', self.database.load_all_players())
        self.menu.add('auto', 'Liste des tournois clôturés', self.database.load_tournament_from_db())
        user_choice = self.menu_view.get_user_choice()
        return user_choice


    #def player_rapports(self):

