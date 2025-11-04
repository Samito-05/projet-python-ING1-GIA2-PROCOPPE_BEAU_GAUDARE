from python.visuals import clear_screen
from python.admin_functions import add_movie, add_room, add_representation, assign_representation_to_room

def admin_menu(admin_user):
    while True:
        clear_screen()
        print(f"Menu Administration - {admin_user.prenom} {admin_user.nom} (role={admin_user.role})")
        print("1) Ajouter un film")
        print("2) Ajouter une salle")
        print("3) Ajouter une représentation")
        print("4) Attribuer une représentation à une salle")
        print("0) Retour au menu principal")
        print("\n")
        choix = input("Choix: ").strip()
        if choix == "1":
            add_movie()
        elif choix == "2":
            add_room()
        elif choix == "3":
            add_representation()
        elif choix == "4":
            assign_representation_to_room()
        elif choix == "0":
            break
        else:
            print("Choix invalide.")
            input("Appuyez sur Entrée pour revenir au menu...")