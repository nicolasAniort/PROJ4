from models.player import Player 
from controllers.player_controller import PlayerController
class PlayerView():
    
    """ initialisation du constructeur de joueur"""
    def __init__(self):
        pass        
    
    
    """Affiche le formulaire de création de joueur et l'enregistre dans la base de données"""
    def show_create_player(self):
        
        print("---------------------------------------------------------------------|")
        print("Création d'un joueur")
        print("---------------------------------------------------------------------|")
        last_name = input("Nom de famille: ")
        first_name = input("Prénom: ")
        national_id = input("Identifiant national: ")
        birth_date = input("Date de naissance (jj/mm/aaaa): ")
        rank = 0
        player: Player = Player(last_name, first_name, birth_date, national_id, rank)
        player_creation = PlayerController.write_player(player)
        return player_creation
        
    def update_rank(self):
        
        print("---------------------------------------------------------------------|")
        print("Mise à jour du classement du joueur")
        print("---------------------------------------------------------------------|")
        print("Entrez les informations de recherche du joueur")
        last_name = input("Nom de famille: ")
        first_name = input("Prénom: ") 
        search_criteria = {'nom':last_name, 'prenom':first_name}
        file_path_players = "data/player_data.json"
        new_search = PlayerController.search_player(file_path_players, search_criteria)
        return new_search
    
    def display_player_register(self):
        print("Le joueur a bien été créé et ajouté dans la base de données")

    def display_enter_player_ranking(self, index: str ):
        print("Entrer le nouveau classement du joueur, identifiant national N° : " + str(index))
    
    def display_player_score_updated(self, index: str):

        print("Le joueur , dont l'identifiant national " + str(index) + "la bien été mis à jour")
