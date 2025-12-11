from typing import Dict, Any, List
from datetime import datetime, timedelta
from python.models import Film, Salle_info, Representation
import storage


def add_movie():
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

def add_room():
    numero = int(input("Numéro de la salle: "))
    nombre_rangees_total = int(input("Nombre total de rangées: "))
    nombre_rangees_vip = int(input("Nombre de rangées VIP: "))
    nombre_colonnes = int(input("Nombre de colonnes: "))
    salle = Salle_info(numero=numero, nombre_rangees_total=nombre_rangees_total,
                    nombre_rangees_vip=nombre_rangees_vip, nombre_colonnes=nombre_colonnes)
    storage.add_salle(salle)
    print(f"Salle numéro {numero} ajoutée avec succès.")
    input("Appuyez sur Entrée pour revenir au menu...")


def calculer_heure_fin(horaire_debut: str, duree: int) -> str:
    debut = datetime.strptime(horaire_debut, "%H:%M")
    fin = debut + timedelta(minutes=duree)
    return fin.strftime("%H:%M")

def add_representation():
    films = storage.list_films()
    if not films:
        print("Aucun film disponible.")
        input("\nAppuyez sur Entrée pour revenir au menu...")
        return
    print("\nFilms disponibles :")
    for i, film in enumerate(films, start=1):
        print(f"{i}. {film.titre}")

    while True:
        try:
            choix_film = int(input("\nEntrez le numéro du film : "))
            if 1 <= choix_film <= len(films):
                film = films[choix_film - 1]
                break
            else:
                print(f"Veuillez entrer un numéro entre 1 et {len(films)}.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

    horaires = getattr(film, "horaires", [])
    if not horaires:
        print(f"\nAucun horaire disponible pour le film '{film.titre}'.")
        return

    print(f"\nHoraires disponibles pour '{film.titre}' :")
    for i, h in enumerate(horaires, start=1):
        print(f"{i}. {h}")

    while True:
        try:
            choix_h = int(input("\nEntrez le numéro de l’horaire : "))
            if 1 <= choix_h <= len(horaires):
                horaire = horaires[choix_h - 1]
                break
            else:
                print(f"Veuillez entrer un numéro entre 1 et {len(horaires)}.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

    horaire_fin=calculer_heure_fin(horaire, film.duree)
    representation_id = f"{film.id}_{horaire}_{horaire_fin}"
    if storage.get_representation(representation_id):
        print(f"\nLa représentation pour '{film.titre}' à {horaire} existe déjà.")
        input("\nAppuyez sur Entrée pour revenir au menu...")
        return
    representation = Representation(film_id=film.id, horaire=horaire, id=representation_id, horaire_fin=horaire_fin)
    storage.add_representation(representation)

    print(f"\nReprésentations '{representation_id}' ajoutée avec succès pour '{film.titre}' à {horaire}.")
    input("\nAppuyez sur Entrée pour revenir au menu...")


def assign_representation_to_room():
    """Permet d'assigner une représentation à une salle via une sélection numérotée."""
    representations = storage.list_representations()
    if not representations:
        print("Aucune représentation disponible.")
        input("\nAppuyez sur Entrée pour revenir au menu...")
        return

    print("\nReprésentations disponibles :")
    for i, rep in enumerate(representations, start=1):
        # On récupère le titre du film pour affichage plus clair
        film = storage.get_film(rep.film_id)
        film_titre = film.titre if film else "Film inconnu"
        print(f"{i}. {film_titre} à {rep.horaire}")

    # Choix de la représentation
    while True:
        try:
            choix_rep = int(input("\nEntrez le numéro de la représentation : "))
            if 1 <= choix_rep <= len(representations):
                representation = representations[choix_rep - 1]
                break
            else:
                print(f"Veuillez entrer un numéro entre 1 et {len(representations)}.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

    # Liste des salles disponibles
    salles = storage.list_salles()
    if not salles:
        print("Aucune salle disponible.")
        input("\nAppuyez sur Entrée pour revenir au menu...")
        return

    print("\nSalles disponibles :")
    for i, salle in enumerate(salles, start=1):
        print(f"{i}. Salle {salle.numero}")

    # Choix de la salle
    while True:
        try:
            choix_salle = int(input("\nEntrez le numéro de la salle : "))
            if 1 <= choix_salle <= len(salles):
                salle = salles[choix_salle - 1]
                break
            else:
                print(f"Veuillez entrer un numéro entre 1 et {len(salles)}.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

    # Assignation
    storage.assign_representation_to_room(representation.id, salle.id)

    print(f"\nReprésentations '{representation.id}' assignée à la salle numéro {salle.numero} avec succès.")
    input("\nAppuyez sur Entrée pour revenir au menu...")

def room_map(representation_id: str, salle_id: str) -> List[List[str]]:
    """Retourne la carte 2D des sièges pour une représentation dans une salle.

    La carte est une liste de listes (rows x cols) contenant 'o' (disponible) ou 'x' (réservé).
    """
    # Récupère l'entrée de salle correspondant à la représentation
    salles_entry = storage.get_salle_seating(salle_id, representation_id)
    if salles_entry is None:
        print(f"Aucune carte trouvée pour la représentation {representation_id} dans la salle {salle_id}.")
        return []
    return getattr(salles_entry, 'seating_map', [])
