from python.visuals import clear_screen
from python.user_functions import list_films, buy_ticket, profile_personnel_info

def user_menu(user):
    while True:
        clear_screen()
        print(f"Menu Utilisateur - {user.prenom} {user.nom} (role={user.role})")
        print("1) Voir les films disponibles")
        print("2) Réserver une salle")
        print("3) Voir mes informations personnelles")
        print("0) Retour au menu principal")
        print("\n")
        choix = input("Choix: ").strip()
        if choix == "1":
            list_films()
        elif choix == "2":
            buy_ticket()
        elif choix == "3":
            profile_personnel_info(user)
        elif choix == "0":
            break
        else:
            print("Choix invalide.")
            input("Appuyez sur Entrée pour revenir au menu...")