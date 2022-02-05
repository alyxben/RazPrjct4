class MenuEntry:
    def __init__(self, option, handler):
        self.option = option
        self.handler = handler

    def __repr__(self):
        return f"MenuEntry({self.option}, {self.handler}"

    def __str__(self):
        return str(self.option)


class MenuModel:
    def __init__(self):
        self._entries = {}
        self._autokey = 1

    def add(self, key, option, handler):
        if key == 'auto':
            key = str(self._autokey)
            self._autokey += 1

        self._entries[str(key)] = MenuEntry(option, handler)

    def items(self):
        return self._entries.items()

    def __contains__(self, user_selection):
        """
        check that user's selection is a valid key
        :param user_selection: user's input
        :return: True if valid selection
        """
        return str(user_selection) in self._entries

    def __getitem__(self, user_selection):
        """
        use the input as key to get the right option
        :param user_selection: user's input
        :return: the item corresponding to the user selection
        """
        return self._entries[user_selection]
