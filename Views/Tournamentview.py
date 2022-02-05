from uuid import uuid4
from typing import Dict
from Models.Matchmodel import Match


class TournamentView:
    def __init__(self):
        pass

    @staticmethod
    def get_player_info():
        tournament_players_info = {}
        players_list = []
        while True:
            try:
                nb_of_players = input("Veuillez entrer le nombre de joueur participant au tournoi:")
                nb_of_players = int(nb_of_players)
                if nb_of_players <= 0:
                    print("Veuillez entrer un nombre entier supérieur à zéro !")
                    continue
            except ValueError:
                print("Veuillez entrer un nombre entier")
                continue
            else:
                break
        for i in range(nb_of_players):
            tournament_players_info['first_name'] = input(f"Veuilez entrer le prénom du joueur {i + 1} :").strip().capitalize()
            tournament_players_info['last_name'] = input(f"Veuillez entrer le nom du joueur {i + 1} :").strip().upper()
            tournament_players_info['age'] = input(f"Veuillez entrer l'age du joueur {i + 1} :").strip()
            tournament_players_info['gender'] = input(f"Veuillez entrer le sexe du joueur {i + 1} :").strip()
            tournament_players_info['birth_date'] = input(
                f"Veuillez entrer la date de naissance du joueur {i + 1} (D/M/Y):").strip()
            while True:
                try:
                    tournament_players_info['rank'] = int(input(f"Veuillez entrer le classement du joueur {i + 1}:"))
                    if tournament_players_info['rank'] <= 0:
                        print("Je n'ai pas compris, veuillez entrer un nombre supérieur à 0")
                        continue
                except ValueError:
                    print("Je n'ai pas compris, veuillez entrer un nombre supérieur à 0")
                    continue
                else:
                    break
            tournament_players_info['id'] = str(uuid4())
            tournament_players_info['elo'] = 0
            players_list.append(dict(tournament_players_info))
        return players_list

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
            tournament_info['nb_of_rounds'] = input(
                "Veuillez entrer le nombre de round souhaité (valeur par defaut 4):").strip()
            if tournament_info['nb_of_rounds'] == "":
                break
            elif tournament_info['nb_of_rounds'].isdigit() is False :
                print('Veuillez entrer un nombre ')
            elif int(tournament_info['nb_of_rounds']) < 1:
                print(f"Veuillez entrer un nombre positif :{tournament_info['nb_of_rounds']} n'est pas un chiffre positif")
            else:
                break
        tournament_info['tournament_players'] = []
        tournament_info['id'] = str(uuid4())
        return tournament_info

    def get_tournament_name(self):
        tournament_name = input(f"Veuillez entrer le nom du tournoi: ").strip()
        return tournament_name


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
            user_input = input(f"Veuillez entrer le nom du tournoi que vous souhaitez continuer:").strip().capitalize()
            if user_input not in live_tournament_names:
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

