from python.visuals import clear_screen
from python.user_functions import (
    list_films, 
    buy_ticket, 
    profile_personnel_info, 
    view_my_reservations,
    search_films
)

def user_menu(user):
    """Menu principal pour les utilisateurs"""
    while True:
        clear_screen()
        print(f"Menu Utilisateur - {user.prenom} {user.nom}")
        print("\n=== FILMS ===")
        print("1) Voir les films disponibles")
        print("2) Rechercher un film")
        print("\n=== RÉSERVATIONS ===")
        print("3) Réserver une place")
        print("4) Voir mes réservations")
        print("\n=== COMPTE ===")
        print("5) Voir mes informations personnelles")
        print("\n0) Retour au menu principal")
        print("\n")
        choix = input("Choix: ").strip()
        
        if choix == "1":
            list_films()
        elif choix == "2":
            search_films()
        elif choix == "3":
            buy_ticket(user)
        elif choix == "4":
            view_my_reservations(user)
        elif choix == "5":
            profile_personnel_info(user)
        elif choix == "0":
            break
        else:
            print("Choix invalide.")
            input("Appuyez sur Entrée pour revenir au menu...")