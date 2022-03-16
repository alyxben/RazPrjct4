from operator import attrgetter


class RapportView:
    def __init__(self):
        pass

    @staticmethod
    def display_players_list(players_list):
        """
        Displays players list by alpha order, or by rank
        :param players_list: List of players displayed
        :return: user choice when he wants out
        """
        possible_answers = ["A", "C", "0"]
        while True:
            try:
                user_choice = input(
                    "Afficher la liste des joueurs par ordre alphabetique (a),\n"
                    "Afficher la liste des joueurs par classement (c),"
                    " 0 pour revenir au menu précédent"
                ).capitalize()
                if user_choice not in possible_answers:
                    print(
                        "Je n'ai pas compris votre réponse, veuillez choisir 'a' pour une liste par ordre\n"
                        " alphabetique ou 'c' pour un classement ou bien  0 pour revenir au menu précédent"
                    )
                    continue
                elif user_choice == possible_answers[0]:
                    print(sorted(players_list, key=attrgetter("last_name")))
                    continue
                elif user_choice == possible_answers[1]:
                    print(
                        sorted(
                            players_list,
                            key=attrgetter("tournament_points"),
                            reverse=True,
                        )
                    )
                    continue
                elif user_choice == possible_answers[2]:
                    return user_choice
            except ValueError:
                print(f"Les choix possibles sont {possible_answers}")
                continue

    @staticmethod
    def get_user_tournament_choice_from_list(tournaments_list):
        """
        Displays tournaments list, get's user input
        :param tournaments_list: Closed tournament list
        :return: Tournament object and user input
        """
        tournaments_name = []
        possible_choices = ["J", "R", "M", "0"]
        print("Liste des tournois clôturés: ")
        print()
        for i in tournaments_list:
            print(i)
            print()
            tournaments_name.append(i.name)
        while True:
            user_input = input(
                "Veuillez entrer le nom du tournoi dont vous souhaitez afficher les "
                "informations"
            ).strip()
            if user_input == "0":
                return user_input
            elif user_input not in tournaments_name:
                print(f"{user_input} n'est pas dans la liste des tournois clôturés")
            else:
                tournament = next(i for i in tournaments_list if i.name == user_input)
            second_input = input(
                "'J' pour afficher les Joueurs de ce tournoi\n"
                "'R' pour afficher les Rounds de ce tournoi\n"
                "'M' pour afficher les Matchs de ce tournoi\n"
            ).capitalize()
            if second_input not in possible_choices:
                print(
                    "Je n'ai pas compris votre demande, 'J' pour Joueurs, 'R' pour Round et 'M' pour Match"
                )
            else:
                return tournament, second_input

    @staticmethod
    def display_round_list(round_list):
        """
        Display round list
        :param round_list: List of rounds played
        """
        n = 1
        for r in round_list:
            print(f"Round: {n}", r)
            n += 1

    @staticmethod
    def display_matchs(match_list):
        """
        Display match list
        :param match_list: List of match already played
        :return:
        """
        for m in match_list:
            print(m)
        print(len(match_list))
