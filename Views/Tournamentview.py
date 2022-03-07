from uuid import uuid4
from typing import Dict
from Models.Tournamentmodel import Tournament


class TournamentView:
    def __init__(self):
        pass

    @staticmethod
    def get_tournament_info():
        """
        display form and gets tournament information
        :return: tournament information as dict
        """

        tournament_info: Dict[str, str] = {
            'name': input("Veuillez entrer le nom du tournoi: ").strip().capitalize(),
            'location': input("Veuillez entrer le lieu du tournoi: ").strip().capitalize(),
            'description': input(
                "Veuillez entrer une description pour ce tournoi: ").strip().capitalize()}
        while True:
            tournament_info['time_set'] = input("Veuillez entrer le type de controle du temps"
                                                " voulu pour ce tournoi (Bullet, Blitz ou Coup rapide)").strip().capitalize()
            if tournament_info['time_set'] not in ('Bullet', 'Blitz', 'Coup rapide'):
                print("Veuillez choisir entre Bullet, Blitz ou coup rapide")
            else:
                break
        while True:
            tournament_info['nb_of_round'] = input(
                "Veuillez entrer le nombre de round souhaité (valeur par defaut 4):").strip()
            if tournament_info['nb_of_round'] == "":
                break
            elif tournament_info['nb_of_round'].isdigit() is False:
                print('Veuillez entrer un nombre ')
            elif int(tournament_info['nb_of_round']) < 1:
                print(
                    f"Veuillez entrer un nombre entier positif :{tournament_info['nb_of_round']} n'est pas un chiffre entier positif")
            else:
                break
        tournament_info['tournament_players_id'] = []
        tournament_info['tournament_id'] = str(uuid4())
        tournament_info['actual_round'] = 0
        tournament_info['round_list'] = []
        tournament_info['begin_date'] = ""
        tournament_info['end_date'] = False
        return tournament_info

    @staticmethod
    def continue_tournament(tournament):
        possible_answers = ['Oui', 'Non']
        while True:
            user_input = input(f"Commencer ou reprendre le tournoi {tournament.name}"
                               f"?(Oui ou Non)").strip().capitalize()
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
        live_tournament_names = []
        print("Liste des tournois en cours: ")
        for i in tournaments_list:
            print(i)
            live_tournament_names.append(i.name)
        while True:
            user_input = input(f"Veuillez entrer le nom du tournoi que vous souhaitez continuer, 0 pour revenir au "
                               f"menu principal: \n").strip().capitalize()
            if user_input == "0":
                return user_input
            elif user_input not in live_tournament_names:
                print(f"{user_input} n'est pas dans la liste des tournois en cours")

            else:
                return next(i.tournament_id for i in tournaments_list if i.name == user_input)

    @staticmethod
    def get_match_result(match):
        possible_input = ['0', '0.5', '1']
        p1 = match[0][0].last_name
        p2 = match[1][0].last_name
        print(p1, 'VS', p2)
        while True:
            try:
                score_p1 = input(f"Veuillez entrer le résultat du joueur {p1}")
                score_p2 = input(f"Veuillez entrer le résultat du joueur {p2}")
                if score_p1 and score_p2 not in possible_input:
                    print("Je n'ai pas compris votre réponse, veuillez entrer 1 si le joueur a gagné, 0 si il a perdu et"
                            " 0.5 pour un match nul ")
                    continue
                else:
                    break
            except ValueError:
                print("Je n'ai pas compris ")
                continue
        match[0].append(float(score_p1))
        match[1].append(float(score_p2))
        return match
