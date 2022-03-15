class MenuEntry:
    def __init__(self, option, handler):
        self.option = option
        self.handler = handler

    def __repr__(self):
        return f"MenuEntry({self.option}, {self.handler}"

    def __str__(self):
        return str(self.option)


class MenuModel():
    def __init__(self):
        self._entries = {}
        self._autokey = 1

    def add_option(self, key, option, handler):
        """
        Adds a menu option
        :param key: used as key for selecting corresponding option
        :param option: option displayed to the user, loaded to MenuEntry
        :param handler: controller corresponding to the user's choice, loaded to MenuEntry
        """
        if key == 'auto':
            key = str(self._autokey)
            self._autokey += 1

        self._entries[str(key)] = MenuEntry(option, handler)

    def items(self):
        return self._entries.items()

    def __contains__(self, user_selection):
        """
        check if user selection is in self._entries
        :param user_selection: user's input
        :return: bool
        """
        return str(user_selection) in self._entries

    def __getitem__(self, user_selection):
        """
        :param user_selection: user's input
        :return: MenuEntry object corresponding to the user's selection
        """
        return self._entries[user_selection]
