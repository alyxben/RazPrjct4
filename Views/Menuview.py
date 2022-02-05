
class HomeMenuView:

    def __init__(self, menu):
        self.menu = menu

    def _display_menu(self):
        """
        private method used to display menu in get_user_choice
        :return:
        """
        for key, entry in self.menu.items():
            print(f"{key}: {entry.option}")
        print()

    def get_user_choice(self):
        """
        displays the menu and gets user selection
        """
        while True:
            self._display_menu()
            user_selection = input('>> ')
            if user_selection in self.menu:
                return self.menu[user_selection]
            else:

                print("Selection Invalide")
