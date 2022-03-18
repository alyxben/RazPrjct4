from uuid import uuid4
from typing import Dict


class TournamentView:
    def __init__(self):
        pass

    @staticmethod
    def get_tournament_info():
        """
        Gets tournament info from user input
        :return: tournament information as dict
        """

        tournament_info: Dict[str, str] = {
            "name": input("Veuillez entrer le nom du tournoi: ").strip().capitalize(),
            "location": input("Veuillez entrer le lieu du tournoi: ")
                .strip()
                .capitalize(),
            "description": input("Veuillez entrer une description pour ce tournoi: ")
                .strip()
                .capitalize(),
        }
        while True:
            tournament_info["time_set"] = (
                input(
                    "Veuillez entrer le type de controle du temps"
                    " voulu pour ce tournoi"
                    " (Bullet, Blitz ou Coup rapide)"
                )
                    .strip()
                    .capitalize()
            )
            if tournament_info["time_set"] not in ("Bullet", "Blitz", "Coup rapide"):
                print("Veuillez choisir entre Bullet, Blitz ou coup rapide")
            else:
                break
        while True:
            tournament_info["nb_of_round"] = input(
                "Veuillez entrer le nombre de round souhaité (valeur par defaut 4):"
            ).strip()
            if tournament_info["nb_of_round"] == "":
                break
            elif tournament_info["nb_of_round"].isdigit() is False:
                print("Veuillez entrer un nombre ")
            elif int(tournament_info["nb_of_round"]) < 1:
                print(
                    f"Veuillez entrer un nombre entier positif :{tournament_info['nb_of_round']}"
                    f" n'est pas un chiffre entier positif"
                )
            else:
                break
        tournament_info["tournament_players_id"] = []
        tournament_info["tournament_id"] = str(uuid4())
        tournament_info["round_id"] = 0
        tournament_info["round_list"] = []
        tournament_info["begin_date"] = ""
        tournament_info["end_date"] = False
        return tournament_info

    @staticmethod
    def continue_tournament(tournament):
        """
        Displays tournament name, and ask user input if he want's to continue it or not
        :param tournament: Tournament object
        :return: True if yes and False if no
        """
        possible_answers = ["Oui", "Non"]
        while True:
            user_input = (
                input(
                    f"Commencer ou reprendre le tournoi {tournament.name} (Oui ou Non)"
                )
                    .strip()
                    .capitalize()
            )
            if user_input not in possible_answers:
                print("Je n'ai pas compris votre réponse, veuillez choisir oui ou non")
            else:
                break
        if user_input == possible_answers[0]:
            return True
        else:
            return False

    @staticmethod
    def get_user_tournament_choice_from_list(tournaments_list):
        """
        Displays tournament list, get user's input, compare it to the tournaments names
        and returns the choosen tournament id
        :param tournaments_list: List of Tournament object
        :return: Tournament object
        """
        live_tournament_names = []
        print("Liste des tournois: ")
        for i in tournaments_list:
            print(i)
            print()
            live_tournament_names.append(i.name)
        while True:
            user_input = input(
                "Veuillez entrer le nom du tournoi, 0 pour revenir au "
                "menu précédent: \n"
            ).strip()
            if user_input == "0":
                return user_input
            elif user_input not in live_tournament_names:
                print(f"{user_input} n'est pas dans la liste des tournois")

            else:
                return next(i for i in tournaments_list if i.name == user_input)

    @staticmethod
    def get_match_result(match):
        """
        Displays match and Gets match result from user input
        :param match: tuple containing match as ([p1], [p2])
        :return: ([p1, score_p1],[p2, score_p2])
        """
        possible_input = ["0", "0.5", "1"]
        p1 = match[0][0]
        p2 = match[1][0]
        print(p1.last_name, "VS", p2.last_name)
        while True:
            try:
                score_p1 = input(
                    f"Veuillez entrer le résultat du joueur {p1.last_name}"
                ).strip()
                score_p2 = input(
                    f"Veuillez entrer le résultat du joueur {p2.last_name}"
                ).strip()
                if score_p1 not in possible_input:
                    print(
                        "Je n'ai pas compris votre réponse, 1 pour une victoire, 0 pour une défaite"
                        " et 0.5 pour une partie nulle"
                    )
                    continue
                elif score_p2 not in possible_input:
                    print(
                        "Je n'ai pas compris votre réponse, 1 pour une victoire, 0 pour une défaite"
                        " et 0.5 pour une partie nulle"
                    )
                    continue
                elif float(score_p1) + float(score_p2) != 1:
                    print("Score non réglementaire, une partie vaut 1 point")
                    continue
                else:
                    break
            except ValueError:
                print("Je n'ai pas compris ")
                continue
        match[0].append(float(score_p1))
        match[1].append(float(score_p2))
        return match

    @staticmethod
    def display_tournament_info(tournament, round, players):
        """Displays tournament round info
        :return user input"""
        match_display_list = []
        for match in round.match_list:
            p1_name = match[0][0].last_name
            p2_name = match[1][0].last_name
            match_display_list.append(f"{p1_name} VS {p2_name}")
        print(
            f"Round: {tournament.round_id + 1}\n"
            f"Le round a commencé le {round.start_time}\n"
            f"Classement:"
        )
        print("{:16.16} | {:4.4} | {}".format("Nom du joueur", "elo", "points"))
        for p in players:
            player_row = "{0:<16.16} | {1: <4.4} | {2}".format(
                p.last_name, str(p.elo), p.tournament_points
            )
            print(player_row)
        print("Liste des matchs: ")
        for m in match_display_list:
            print(m)
        while True:
            user_input = input(
                f"Appuyer sur Enter pour mettre fin au round {tournament.round_id + 1} "
                f"et entrer les résultats, 0 pour revenir au menu principal: "
            )
            if user_input not in ["", "0"]:
                print("je n'ai pas compris votre réponse")
            else:
                return user_input

    @staticmethod
    def display_end_tournament(tournament, players_ranking):
        """Displays finished tournament info"""
        print(tournament)
        print(
            "Classement: "
        )
        print("{:16.16} | {:4.4} | {}".format("Nom du joueur", "elo", "points"))
        for p in players_ranking:
            player_row = "{0:<16.16} | {1: <4.4} | {2}".format(
                p.last_name, str(p.elo), p.tournament_points
            )
            print(player_row)
        while True:
            user_input = input("Appuyer sur Enter pour revenir au menu principal: ")
            if user_input != "":
                print("Je n'ai pas compris votre demande")
                continue
            else:
                break
