from operator import attrgetter


class RapportView:
    def __init__(self):
        pass

    def display_players_list(self, players_list):
        possible_answers = ['A', 'C']
        while True:
            user_choice = input("Afficher la liste des joueurs par ordre alphabetique (a),\n"
                                "Afficher la liste des joueurs par classement (c)").capitalize()
            if user_choice not in possible_answers:
                print("Je n'ai pas compris votre réponse, veuillez choisir 'a' pour une liste par ordre\n"
                      " alphabetique ou 'c' pour un classement  ")
            elif user_choice == possible_answers[0]:
                print(sorted(players_list, key=attrgetter('last_name')))
            elif user_choice == possible_answers[1]:
                print(sorted(players_list, key=attrgetter('elo'), reverse=True))

    def get_user_tournament_choice_from_list(self, tournaments_list):
        live_tournament_names = []
        possible_choices = ['J', 'R', 'M']
        print("Liste des tournois clôturés: ")
        for i in tournaments_list:
            print(i)
            live_tournament_names.append(i.name)
        while True:
            user_input = input(f"Veuillez entrer le nom du tournoi dont vous souhaitez afficher les "
                               f"informations").strip().capitalize()
            if user_input == "0":
                return user_input
            elif user_input not in live_tournament_names:
                print(f"{user_input} n'est pas dans la liste des tournois clôturés")
            else:
                tournament = next(i for i in tournaments_list if i.name == user_input)
            second_input = input(f"'J' pour afficher les Joueurs de ce tournoi\n"
                                 f"'R' pour afficher les Rounds de ce tournoi\n"
                                 f"'M' pour afficher les Matchs de ce tournoi\n")
            if second_input not in possible_choices:
                print("Je n'ai pas compris votre demande, 'J' pour Joueurs, 'R' pour Round et 'M' pour Match")
            else:
                return tournament, second_input

    def display_round_list(self, round_list):
        print(round_list)

    def display_matchs(self, match_list):
        for m in match_list:
            print(m)