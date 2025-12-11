from python.visuals import clear_screen
from python.admin_functions import (
    add_movie, 
    add_room, 
    add_representation, 
    assign_representation_to_room,
    view_all_reservations,
    view_statistics,
    remove_film,
    remove_room,
    remove_representation
)

def admin_menu(user):
    """Menu principal pour les administrateurs"""
    while True:
        clear_screen()
        print(f"Menu Administrateur - {user.prenom} {user.nom}")
        print("\n=== GESTION DES FILMS ===")
        print("1) Ajouter un film")
        print("2) Supprimer un film")
        print("\n=== GESTION DES SALLES ===")
        print("3) Ajouter une salle")
        print("4) Supprimer une salle")
        print("\n=== GESTION DES REPRÉSENTATIONS ===")
        print("5) Ajouter une représentation")
        print("6) Assigner une représentation à une salle")
        print("7) Supprimer une représentation")
        print("\n=== RÉSERVATIONS ET STATISTIQUES ===")
        print("8) Voir toutes les réservations")
        print("9) Voir les statistiques")
        print("\n0) Retour au menu principal")
        print("\n")
        choix = input("Choix: ").strip()
        
        if choix == "1":
            add_movie()
        elif choix == "2":
            remove_film()
        elif choix == "3":
            add_room()
        elif choix == "4":
            remove_room()
        elif choix == "5":
            add_representation()
        elif choix == "6":
            assign_representation_to_room()
        elif choix == "7":
            remove_representation()
        elif choix == "8":
            view_all_reservations()
        elif choix == "9":
            view_statistics()
        elif choix == "0":
            break
        else:
            print("Choix invalide.")
            input("Appuyez sur Entrée pour revenir au menu...")