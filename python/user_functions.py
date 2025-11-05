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

def profile_personnel_info(user: Utilisateur):
    clear_screen()
    print("Informations personnelles:")
    print(f"Nom: {user.nom}")
    print(f"Prénom: {user.prenom}")
    print(f"Rôle: {user.role}")
    print(f"Email: {user.email}")
    print("\n")
    print("1) Modifier mes informations personnelles")
    print("0) Retour au menu principal")
    choix = input("Choix: ").strip()
    if choix == "1":
        modif_profile_personnel_info(user)
    elif choix == "0":
        return
    else:
        print("Choix invalide.")
        input("Appuyez sur Entrée pour revenir au menu...")

def modif_profile_personnel_info(user):
    clear_screen()
    print("Modifier mes informations personnelles:")
    new_nom = input(f"Nom ({user.nom}): ") or user.nom
    new_prenom = input(f"Prénom ({user.prenom}): ") or user.prenom
    new_email = input(f"Email ({user.email}): ") or user.email

    user.nom = new_nom
    user.prenom = new_prenom
    user.email = new_email

    storage.update_utilisateur(user)
    print("Informations mises à jour avec succès.")
    input("Appuyez sur Entrée pour revenir au menu...")