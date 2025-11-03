from python.models import Film, Salle, Utilisateur
from python.visuals import ascii_art, clear_screen
import storage

def user_menu(user):
    while True:
        clear_screen()
        print(f"Menu Utilisateur - {user.prenom} {user.nom} (role={user.role})")
        print("1) Voir les films disponibles")
        print("2) Réserver une salle")
        print("0) Retour au menu principal")
        print("\n")
        choix = input("Choix: ").strip()
        if choix == "1":
            films = storage.list_films()
            if not films:
                print("\n")
                print("Aucun film.")
            for f in films:
                print(f"- {f.titre} ({f.duree}min) [{f.categorie}] Age minimum={f.age_min} ")
            print("\n")
            input("Appuyez sur Entrée pour revenir au menu...")
        elif choix == "2":
            print("Fonctionnalité de réservation de salle à implémenter.")
            input("Appuyez sur Entrée pour revenir au menu...")
        elif choix == "0":
            break
        else:
            print("Choix invalide.")
            input("Appuyez sur Entrée pour revenir au menu...")