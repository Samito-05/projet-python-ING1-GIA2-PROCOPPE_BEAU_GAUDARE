from python.models import Film, Salle_info, Utilisateur
from python.visuals import ascii_art, clear_screen
import storage

def list_films():
    films = storage.list_films()
    if not films:
        print("\n")
        print("Aucun film.")
    for f in films:
        print(f"- {f.titre} ({f.duree}min) [{f.categorie}] Age minimum={f.age_min} ")
    print("\n")
    input("Appuyez sur Entrée pour revenir au menu...")

def buy_ticket():
    print("Fonctionnalité de réservation de salle à implémenter.")
    input("Appuyez sur Entrée pour revenir au menu...")

