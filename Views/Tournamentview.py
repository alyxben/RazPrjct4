from uuid import uuid4
from typing import Dict
from Models.Matchmodel import Match


class TournamentView:
    def __init__(self):
        pass

    @staticmethod
    def get_tournament_info():
        """
        display form and gets tournament information
        :return: tournament information as dict
        """

        tournament_info: Dict[str, str] = {'tournament_name': input("Veuillez entrer le nom du tournoi: ").strip().capitalize(),
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
            elif tournament_info['nb_of_round'].isdigit() is False :
                print('Veuillez entrer un nombre ')
            elif int(tournament_info['nb_of_round']) < 1:
                print(f"Veuillez entrer un nombre entier positif :{tournament_info['nb_of_round']} n'est pas un chiffre entier positif")
            else:
                break
        tournament_info['tournament_players'] = []
        tournament_info['tournament_id'] = str(uuid4())
        return tournament_info

    def continue_tournament(self, tournament_name):
        possible_answers = ['Oui', 'Non']
        while True:
            user_input = input(f"Commencer ou reprendre le tournoi {tournament_name}"
                               f"?(Oui ou Non)").strip().capitalize()
            if user_input not in possible_answers:
                print("Je n'ai pas compris votre réponse, veuillez choisir oui ou non")
            else:
                break
        if user_input == possible_answers[0]:
            return True
        else:
            return False

    def get_user_touurnament_choice_from_list(self, tournaments_list):
        live_tournament_names = []
        list_of_tournament_ids = []
        print("Liste des tournois en cours: ")
        user_choice = {}
        for i in tournaments_list:
            print(i)
            live_tournament_names.append(i['tournament_name'])
            list_of_tournament_ids.append(i['tournament_id'])
        while True:
            user_input = input(f"Veuillez entrer le nom du tournoi que vous souhaitez continuer, 0 pour revenir au "
                               f"menu principal: \n").strip().capitalize()
            if user_input == "0":
                return user_input
            elif user_input not in live_tournament_names:
                print(f"{user_input} n'est pas dans la liste des tournois en cours")

            else:
                return next(i for i in tournaments_list if i['tournament_name'] == user_input)


    @staticmethod
    def get_match_result(match):
        possible_input = [match.player1.last_name, match.player2.last_name, 'Nulle']
        while True:
            print(match)
            match_result = input(f"Veuillez entrer le nom du vainqueur, ou nulle pour une partie nulle: ").strip().capitalize()
            if match_result not in possible_input:
                print("Je n'ai pas compris votre réponse")
            else:
                break
        return match_result

