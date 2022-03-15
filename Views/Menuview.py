class HomeMenuView:

    def __init__(self, menu):
        """
        :param menu: MenuModel
        """
        self.menu = menu

    def _display_menu(self):
        """
        displays the menu key and options
        """
        for key, entry in self.menu.items():
            print(f"{key}: {entry.option}")
        print()

    def get_user_choice(self):
        """
        use _display_menu and gets user selection
        :return user's choice
        """
        while True:
            self._display_menu()
            user_selection = input('>> ')
            if user_selection in self.menu:
                return self.menu[user_selection]
            else:
                print("Selection Invalide")
