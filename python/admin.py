from python.models import Film, Salle, Utilisateur
from python.visuals import ascii_art, clear_screen
import storage

def admin_menu(admin_user):
    while True:
        clear_screen()
        print(f"Menu Administration - {admin_user.prenom} {admin_user.nom} (role={admin_user.role})")
        print("1) Ajouter un film")
        print("2) Ajouter une salle")
        print("0) Retour au menu principal")
        print("\n")
        choix = input("Choix: ").strip()
        if choix == "1":
            titre = input("Titre du film: ")
            duree = int(input("Durée (en minutes): "))
            categorie = input("Catégorie: ")
            age_min = int(input("Âge minimum: "))
            nbr_representations = int(input("Nombre de représentations par jours: "))
            horaires = []
            for i in range(nbr_representations):
                horaire = input(f"Horaire de la représentation {i+1} (HH:MM): ")
                horaires.append(horaire)
            film = Film(titre=titre, duree=duree, categorie=categorie, age_min=age_min, horaires=horaires)
            storage.add_film(film)
            print(f"Film '{titre}' ajouté avec succès.")
            input("Appuyez sur Entrée pour revenir au menu...")
        elif choix == "2":
            numero = int(input("Numéro de la salle: "))
            nombre_rangees_total = int(input("Nombre total de rangées: "))
            nombre_rangees_vip = int(input("Nombre de rangées VIP: "))
            nombre_colonnes = int(input("Nombre de colonnes: "))
            salle = Salle(numero=numero, nombre_rangees_total=nombre_rangees_total,
                          nombre_rangees_vip=nombre_rangees_vip, nombre_colonnes=nombre_colonnes)
            storage.add_salle(salle)
            print(f"Salle numéro {numero} ajoutée avec succès.")
            input("Appuyez sur Entrée pour revenir au menu...")
        elif choix == "0":
            break
        else:
            print("Choix invalide.")
            input("Appuyez sur Entrée pour revenir au menu...")