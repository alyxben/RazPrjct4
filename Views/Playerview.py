from uuid import uuid4

class PlayerView:
    def __init__(self):
        pass

    @staticmethod
    def get_player_info():
        player_info = {}
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
            player_info['first_name'] = input(f"Veuilez entrer le prénom du joueur {i + 1} :").strip().capitalize()
            player_info['last_name'] = input(f"Veuillez entrer le nom du joueur {i + 1} :").strip().upper()
            player_info['age'] = input(f"Veuillez entrer l'age du joueur {i + 1} :").strip()
            player_info['gender'] = input(f"Veuillez entrer le sexe du joueur {i + 1} :").strip()
            player_info['birth_date'] = input(
                f"Veuillez entrer la date de naissance du joueur {i + 1} (D/M/Y):").strip()
            while True:
                try:
                    player_info['rank'] = int(input(f"Veuillez entrer le classement du joueur {i + 1}:"))
                    if player_info['rank'] <= 0:
                        print("Je n'ai pas compris, veuillez entrer un nombre supérieur à 0")
                        continue
                except ValueError:
                    print("Je n'ai pas compris, veuillez entrer un nombre supérieur à 0")
                    continue
                else:
                    break
            player_info['id'] = str(uuid4())
            player_info['elo'] = 0
            players_list.append(dict(player_info))
        return players_list