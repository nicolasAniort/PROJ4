import re
import json
from typing import List
from models.tournament import Tournament
from controllers.player_controller import PlayerController
from views.tournamentview import TournamentView

class TournamentController():

    def __init__(self):
        pass
    """creation d'un tournoi"""
    def create_tournament(self):
        """recuperation de la saisie"""
        input_result :List = TournamentView.show_create_tournament(self)
        tournament_id = 'TR'+ str(re.sub("/", "", input_result[2]))
        tournament_name = str(input_result[0])
        tournament_location = str(input_result[1])
        tournament_date_start = input_result[2]
        tournament_date_end = input_result[3]
        tournament_description = str(input_result[4])
        tournament_number_of_round = 4
        tournament_round_number = 1
        tournament_round_list = []
        tournament_players_list: str = ""
        tournament = Tournament(tournament_id,tournament_name,tournament_location,tournament_date_start,tournament_date_end,tournament_number_of_round,tournament_description,tournament_round_number,tournament_round_list,tournament_players_list)
        
        """Creer un nouveau tournoi """
        tournaments = []
        try:
            with open('data/tournaments/tournament_data.json', 'r') as file:
                tournaments = json.load(file)
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            pass
        new_tournament_name = tournament.tournament_name
        new_tournament_date_start = tournament.tournament_date_start
        new_tournament = {
        "id du tournoi" : tournament.tournament_id,    
        "nom_du_tournoi":tournament.tournament_name,
        "lieu":tournament.tournament_location,
        "date_de_debut":tournament.tournament_date_start,
        "date_de_fin":tournament.tournament_date_end,
        "nombre_de_round":tournament.tournament_number_of_round,
        "description_tournoi":tournament.tournament_description,
        "numero_round_actif":tournament.tournament_round_number,
        "liste_des_rounds":tournament.tournament_round_list,
        "liste_des_joueurs":TournamentController.create_file_player_path(tournament_id)      
        }
        tournaments.append(new_tournament)

        with open('data/tournaments/tournament_data.json', 'w') as file:
            json.dump(tournaments, file,indent=2)
        
        tournament_players = []    
        new_tournament_players_file = {
            "identifiant_nationnal": '',
            "nom_du_joueur" : '',
            "prenom": '',
            "classsement" : ''            
        }
        tournament_players.append(new_tournament_players_file)
        file_path = TournamentController.create_file_player_path(tournament.tournament_id)

        with open(file_path, 'x') as file:
            json.dump(tournament_players, file, indent=2)     
        TournamentView.display_tournament_created(self)
    """Liste des tournois enregistr??s"""           
    def list_registred_tournaments(self):
        """Liste des tournois class??s par ordre alphab??tique"""
        # Charger les donn??es ?? partir du fichier tournament_data.json
        tournament_data = []
        with open("data/tournaments/tournament_data.json", "r") as file:
            file_contents = file.read()
            tournament_data = json.loads(file_contents)
        #tri par ordre alphab??tique
        tournament_data_alphabetical = sorted(tournament_data, key=lambda tournament: tournament["nom_du_tournoi"])
        #appel de la fonction qui cr???? la vue des tournois pour choisir
        TournamentView.list_tournaments_for_choice_view(self, tournament_list= tournament_data_alphabetical)
           
    """Liste des tournois class??s par date"""
    def list_tournament_for_choice(self):
        # Charger les donn??es ?? partir du fichier tournament_data.json
        tournament_data = []
        with open("data/tournaments/tournament_data.json", "r") as file:
            file_contents = file.read()
            tournament_data = json.loads(file_contents)
        #tri par ordre d'anciennet??
        tournament_data_date = []
        tournament_data_date = sorted(tournament_data, reverse=True, key=lambda tournament: tournament["nom_du_tournoi"])
        #appel de la fonction qui cr???? la vue des tournois pour choisir
        selected_index = TournamentView.list_tournaments_for_choice_view(self, tournament_list= tournament_data_date)
        # Acc??s au tournoi s??lectionn??
        selected_tournament = tournament_data_date[TournamentView.display_choice_tournament(self)]
        return selected_tournament    
    
    """methode de creation du chemin d'acc??s au fichier du nouveau tournoi"""
    def create_file_player_path(tournament_id):    
        
        id_string = tournament_id
        file_name = id_string +"_players" + ".json"
        file_path = 'data/tournaments/' + file_name
        return file_path
    """Ajouter un joueur au tournoi choisi"""
    def add_player_to_tournament(self,tournament: Tournament):
        
        national_id_new =TournamentView.display_add_player_to_tournament(self)
        if not national_id_new:
            return None
        player_new = PlayerController.search_player(self, search_criteria = national_id_new)
        fpath = tournament["liste_des_joueurs"]
        tournament_players = []    
        with open(fpath, 'r') as file:
            tournament_players = json.load(file)
            
        #si l'identifiant existe d??j?? dans la basee de donn??es d'inscrits, alors on inscrit automatiquement le joueur
        if player_new != None:
            player_for_tournament = PlayerController.reader_player(self, national_id = national_id_new)
            new_tournament_players_file = {
                "identifiant_nationnal": player_for_tournament.national_id,
                "nom_du_joueur" : player_for_tournament.last_name,
                "prenom": player_for_tournament.first_name,
                "date_de_naissance": player_for_tournament.birth_date,
                "classsement" : player_for_tournament.rank            
            }
            tournament_players.append(new_tournament_players_file)
            PlayerController.update_file_players(self,players = tournament_players,file_path = fpath)
            
        else:
            new_user = PlayerController.write_player(self, path =fpath)
            PlayerController.update_file_players(self,players = new_user,file_path = fpath)
        