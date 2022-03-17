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
                    return
            except ValueError:
                print(f"Les choix possibles sont {possible_answers}")
                continue

    @staticmethod
    def get_user_display_choice(tournament):
        possible_choices = ["J", "R", "M", "0"]
        while True:
            user_input = input(f"J pour afficher les joueurs du tournoi {tournament.name}\n"
                               f"R pour afficher les rounds du tournoi {tournament.name}\n"
                               f"M pour afficher les mathc du tournoi {tournament.name}\n"
                               f"0 pour revenir au menu précédent\n").capitalize()
            if user_input not in possible_choices:
                print(
                    "Je n'ai pas compris votre demande, 'J' pour Joueurs, 'R' pour Round et 'M' pour Match"
                )
                continue
            else:
                return user_input

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
        input("Appuyer sur n'importe quel touche pour retourner au menu précédent")

    @staticmethod
    def display_matchs(match_list):
        """
        Display match list
        :param match_list: List of match already played
        :return:
        """
        for m in match_list:
            print(m)
        print(f"Nombre de match :{len(match_list)}")
        input("Appuyer sur n'importe quel touche pour retourner au menu précédent")
