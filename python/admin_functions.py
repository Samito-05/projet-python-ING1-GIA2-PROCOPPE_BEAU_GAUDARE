from typing import Dict, Any, List
from datetime import datetime, timedelta
from collections import defaultdict
from python.models import Film, Salle_info, Representation
import storage


def add_movie():
    """Ajoute un nouveau film"""
    titre = input("Titre du film: ")
    duree = int(input("Durée (en minutes): "))
    categorie = input("Catégorie: ")
    age_min = int(input("Âge minimum: "))
    nbr_representations = int(input("Nombre de représentations par jour: "))
    horaires = []
    for i in range(nbr_representations):
        horaire = input(f"Horaire de la représentation {i+1} (HH:MM): ")
        horaires.append(horaire)
    film = Film(titre=titre, duree=duree, categorie=categorie, age_min=age_min, horaires=horaires)
    storage.add_film(film)
    print(f"\n✅ Film '{titre}' ajouté avec succès.")
    input("Appuyez sur Entrée pour revenir au menu...")


def remove_film():
    """Supprime un film existant"""
    films = storage.list_films()
    if not films:
        print("\nAucun film à supprimer.")
        input("Appuyez sur Entrée...")
        return
    
    print("\n=== FILMS DISPONIBLES ===\n")
    for i, film in enumerate(films, 1):
        print(f"{i}. {film.titre} ({film.duree}min) [{film.categorie}]")
    
    try:
        choix = int(input("\nEntrez le numéro du film à supprimer (0 pour annuler): "))
        if choix == 0:
            return
        if 1 <= choix <= len(films):
            film = films[choix - 1]
            
            # Vérifier s'il y a des réservations pour ce film
            reservations = storage.list_reservations()
            reservations_film = [r for r in reservations if r.film_id == film.id]
            
            if reservations_film:
                print(f"\n⚠️ Attention: {len(reservations_film)} réservation(s) existe(nt) pour ce film.")
                print("Êtes-vous sûr de vouloir supprimer ce film? (oui/non): ", end="")
                confirmation = input().strip().lower()
                if confirmation != "oui":
                    print("Suppression annulée.")
                    input("Appuyez sur Entrée...")
                    return
            
            # Supprimer le film
            db = storage.load_db()
            db['films'] = [f for f in db.get('films', []) if f.get('id') != film.id]
            
            # Supprimer les représentations associées
            db['representations'] = [r for r in db.get('representations', []) if r.get('film_id') != film.id]
            
            storage.save_db(db)
            print(f"\n✅ Film '{film.titre}' supprimé avec succès.")
        else:
            print("Choix invalide.")
    except ValueError:
        print("Entrée invalide.")
    
    input("Appuyez sur Entrée...")


def add_room():
    """Ajoute une nouvelle salle"""
    numero = int(input("Numéro de la salle: "))
    nombre_rangees_total = int(input("Nombre total de rangées: "))
    nombre_rangees_vip = int(input("Nombre de rangées VIP: "))
    nombre_colonnes = int(input("Nombre de colonnes: "))
    
    if nombre_rangees_vip > nombre_rangees_total:
        print("\n⚠️ Le nombre de rangées VIP ne peut pas dépasser le nombre total de rangées.")
        input("Appuyez sur Entrée...")
        return
    
    salle = Salle_info(numero=numero, nombre_rangees_total=nombre_rangees_total,
                    nombre_rangees_vip=nombre_rangees_vip, nombre_colonnes=nombre_colonnes)
    storage.add_salle(salle)
    print(f"\n✅ Salle numéro {numero} ajoutée avec succès.")
    print(f"   - {nombre_rangees_total} rangées ({nombre_rangees_vip} VIP)")
    print(f"   - {nombre_colonnes} colonnes")
    print(f"   - Capacité totale: {nombre_rangees_total * nombre_colonnes} places")
    input("Appuyez sur Entrée pour revenir au menu...")


def remove_room():
    """Supprime une salle existante"""
    salles = storage.list_salles()
    if not salles:
        print("\nAucune salle à supprimer.")
        input("Appuyez sur Entrée...")
        return
    
    print("\n=== SALLES DISPONIBLES ===\n")
    for i, salle in enumerate(salles, 1):
        capacite = salle.nombre_rangees_total * salle.nombre_colonnes
        print(f"{i}. Salle {salle.numero} - Capacité: {capacite} places")
    
    try:
        choix = int(input("\nEntrez le numéro de la salle à supprimer (0 pour annuler): "))
        if choix == 0:
            return
        if 1 <= choix <= len(salles):
            salle = salles[choix - 1]
            
            # Vérifier s'il y a des représentations assignées
            if salle.id_representations:
                print(f"\n⚠️ Attention: {len(salle.id_representations)} représentation(s) assignée(s) à cette salle.")
                print("Êtes-vous sûr de vouloir supprimer cette salle? (oui/non): ", end="")
                confirmation = input().strip().lower()
                if confirmation != "oui":
                    print("Suppression annulée.")
                    input("Appuyez sur Entrée...")
                    return
            
            # Supprimer la salle
            db = storage.load_db()
            db['salle_info'] = [s for s in db.get('salle_info', []) if s.get('id') != salle.id]
            db['salles'] = [s for s in db.get('salles', []) if s.get('salle_id') != salle.id]
            storage.save_db(db)
            
            print(f"\n✅ Salle {salle.numero} supprimée avec succès.")
        else:
            print("Choix invalide.")
    except ValueError:
        print("Entrée invalide.")
    
    input("Appuyez sur Entrée...")


def calculer_heure_fin(horaire_debut: str, duree: int) -> str:
    """Calcule l'heure de fin à partir de l'heure de début et de la durée"""
    debut = datetime.strptime(horaire_debut, "%H:%M")
    fin = debut + timedelta(minutes=duree)
    return fin.strftime("%H:%M")


def add_representation():
    """Ajoute une nouvelle représentation"""
    films = storage.list_films()
    if not films:
        print("\nAucun film disponible.")
        input("Appuyez sur Entrée pour revenir au menu...")
        return
    
    print("\n=== FILMS DISPONIBLES ===\n")
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
        input("Appuyez sur Entrée...")
        return

    print(f"\n=== HORAIRES POUR '{film.titre}' ===\n")
    for i, h in enumerate(horaires, start=1):
        print(f"{i}. {h}")

    while True:
        try:
            choix_h = int(input("\nEntrez le numéro de l'horaire : "))
            if 1 <= choix_h <= len(horaires):
                horaire = horaires[choix_h - 1]
                break
            else:
                print(f"Veuillez entrer un numéro entre 1 et {len(horaires)}.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

    horaire_fin = calculer_heure_fin(horaire, film.duree)
    representation_id = f"{film.id}_{horaire}_{horaire_fin}"
    
    if storage.get_representation(representation_id):
        print(f"\n⚠️ La représentation pour '{film.titre}' à {horaire} existe déjà.")
        input("Appuyez sur Entrée pour revenir au menu...")
        return
    
    representation = Representation(film_id=film.id, horaire=horaire, id=representation_id, horaire_fin=horaire_fin)
    storage.add_representation(representation)

    print(f"\n✅ Représentation '{representation_id}' ajoutée avec succès pour '{film.titre}' à {horaire}.")
    input("Appuyez sur Entrée pour revenir au menu...")


def remove_representation():
    """Supprime une représentation existante"""
    representations = storage.list_representations()
    if not representations:
        print("\nAucune représentation à supprimer.")
        input("Appuyez sur Entrée...")
        return
    
    print("\n=== REPRÉSENTATIONS DISPONIBLES ===\n")
    for i, rep in enumerate(representations, 1):
        film = storage.get_film(rep.film_id)
        film_titre = film.titre if film else "Film inconnu"
        print(f"{i}. {film_titre} à {rep.horaire} (fin: {rep.horaire_fin})")
    
    try:
        choix = int(input("\nEntrez le numéro de la représentation à supprimer (0 pour annuler): "))
        if choix == 0:
            return
        if 1 <= choix <= len(representations):
            representation = representations[choix - 1]
            
            # Vérifier s'il y a des réservations
            reservations = storage.list_reservations()
            reservations_rep = [r for r in reservations if r.film_id == representation.film_id and r.horaire == representation.horaire]
            
            if reservations_rep:
                print(f"\n⚠️ Attention: {len(reservations_rep)} réservation(s) existe(nt) pour cette représentation.")
                print("Êtes-vous sûr de vouloir supprimer cette représentation? (oui/non): ", end="")
                confirmation = input().strip().lower()
                if confirmation != "oui":
                    print("Suppression annulée.")
                    input("Appuyez sur Entrée...")
                    return
            
            # Supprimer la représentation
            db = storage.load_db()
            db['representations'] = [r for r in db.get('representations', []) if r.get('id') != representation.id]
            
            # Retirer de la liste des salles
            for salle in db.get('salle_info', []):
                if representation.id in salle.get('id_representations', []):
                    salle['id_representations'].remove(representation.id)
            
            # Supprimer l'entrée de carte de sièges
            db['salles'] = [s for s in db.get('salles', []) if representation.id not in s.get('representation_id', [])]
            
            storage.save_db(db)
            print(f"\n✅ Représentation supprimée avec succès.")
        else:
            print("Choix invalide.")
    except ValueError:
        print("Entrée invalide.")
    
    input("Appuyez sur Entrée...")


def assign_representation_to_room():
    """Permet d'assigner une représentation à une salle avec vérification des conflits"""
    representations = storage.list_representations()
    if not representations:
        print("\nAucune représentation disponible.")
        input("Appuyez sur Entrée pour revenir au menu...")
        return

    print("\n=== REPRÉSENTATIONS DISPONIBLES ===\n")
    for i, rep in enumerate(representations, start=1):
        film = storage.get_film(rep.film_id)
        film_titre = film.titre if film else "Film inconnu"
        print(f"{i}. {film_titre} à {rep.horaire} (fin: {rep.horaire_fin})")

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
        print("\nAucune salle disponible.")
        input("Appuyez sur Entrée pour revenir au menu...")
        return

    print("\n=== SALLES DISPONIBLES ===\n")
    for i, salle in enumerate(salles, start=1):
        capacite = salle.nombre_rangees_total * salle.nombre_colonnes
        print(f"{i}. Salle {salle.numero} - Capacité: {capacite} places")

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

    # Assignation avec vérification
    success, error_msg = storage.assign_representation_to_room(representation.id, salle.id)
    
    if success:
        print(f"\n✅ Représentation assignée à la salle numéro {salle.numero} avec succès.")
    else:
        print(f"\n❌ Erreur: {error_msg}")
        print("La représentation n'a pas pu être assignée à cette salle.")
    
    input("Appuyez sur Entrée pour revenir au menu...")


def view_all_reservations():
    """Affiche toutes les réservations avec possibilité de les gérer"""
    from python.visuals import clear_screen
    
    clear_screen()
    print("=== TOUTES LES RÉSERVATIONS ===\n")
    
    reservations = storage.list_reservations()
    
    if not reservations:
        print("Aucune réservation enregistrée.")
        input("\nAppuyez sur Entrée...")
        return
    
    # Grouper par film
    reservations_par_film = defaultdict(list)
    for res in reservations:
        reservations_par_film[res.film_id].append(res)
    
    total_places = 0
    total_revenus = 0.0
    
    for film_id, res_list in reservations_par_film.items():
        film = storage.get_film(film_id)
        film_titre = film.titre if film else "Film inconnu"
        
        print(f"\n🎞️ {film_titre}")
        print("-" * 50)
        
        for res in res_list:
            # Trouver l'utilisateur
            users = storage.list_utilisateurs()
            user = None
            for u in users:
                if u.id == res.utilisateur_id:
                    user = u
                    break
            
            user_nom = f"{user.nom} {user.prenom}" if user else "Utilisateur inconnu"
            salle = storage.get_salle(res.salle_id)
            salle_num = salle.numero if salle else "?"
            
            # Calculer le revenu pour cette réservation
            revenu_res = 0.0
            if salle:
                for place in res.places:
                    row_letter = place[0]
                    row_idx = ord(row_letter) - 65
                    if row_idx < salle.nombre_rangees_vip:
                        revenu_res += 15.0  # Prix VIP
                    else:
                        revenu_res += 10.0  # Prix normal
            
            print(f"  • {user_nom} ({user.email if user else 'N/A'})")
            print(f"    Salle {salle_num} - Horaire: {res.horaire}")
            print(f"    Places: {', '.join(res.places)} ({len(res.places)} place(s))")
            print(f"    Revenu: {revenu_res:.2f}€")
            print(f"    ID: {res.id}")
            
            total_places += len(res.places)
            total_revenus += revenu_res
    
    print("\n" + "=" * 50)
    print(f"TOTAL: {len(reservations)} réservations - {total_places} places - {total_revenus:.2f}€")
    print("=" * 50)
    
    input("\nAppuyez sur Entrée...")


def view_statistics():
    """Affiche des statistiques détaillées sur le cinéma"""
    from python.visuals import clear_screen
    
    clear_screen()
    print("=== STATISTIQUES DU CINÉMA ===\n")
    
    films = storage.list_films()
    salles = storage.list_salles()
    representations = storage.list_representations()
    reservations = storage.list_reservations()
    utilisateurs = storage.list_utilisateurs()
    
    # Statistiques générales
    print("📊 STATISTIQUES GÉNÉRALES")
    print("-" * 50)
    print(f"Films disponibles: {len(films)}")
    print(f"Salles: {len(salles)}")
    print(f"Représentations programmées: {len(representations)}")
    print(f"Utilisateurs inscrits: {len(utilisateurs)}")
    print(f"Réservations totales: {len(reservations)}")
    
    # Capacité totale
    capacite_totale = sum(s.nombre_rangees_total * s.nombre_colonnes for s in salles)
    print(f"Capacité totale: {capacite_totale} places")
    
    # Revenus
    print("\n💰 REVENUS")
    print("-" * 50)
    
    total_revenus = 0.0
    total_places_reservees = 0
    
    for res in reservations:
        salle = storage.get_salle(res.salle_id)
        if salle:
            for place in res.places:
                row_letter = place[0]
                row_idx = ord(row_letter) - 65
                if row_idx < salle.nombre_rangees_vip:
                    total_revenus += 15.0
                else:
                    total_revenus += 10.0
        total_places_reservees += len(res.places)
    
    print(f"Revenus totaux: {total_revenus:.2f}€")
    print(f"Places réservées: {total_places_reservees}")
    if capacite_totale > 0 and len(representations) > 0:
        taux_occupation = (total_places_reservees / (capacite_totale * len(representations))) * 100
        print(f"Taux d'occupation moyen: {taux_occupation:.1f}%")
    
    # Films les plus populaires
    print("\n🎬 FILMS LES PLUS POPULAIRES")
    print("-" * 50)
    
    reservations_par_film = defaultdict(int)
    revenus_par_film = defaultdict(float)
    
    for res in reservations:
        reservations_par_film[res.film_id] += len(res.places)
        
        salle = storage.get_salle(res.salle_id)
        if salle:
            for place in res.places:
                row_letter = place[0]
                row_idx = ord(row_letter) - 65
                prix = 15.0 if row_idx < salle.nombre_rangees_vip else 10.0
                revenus_par_film[res.film_id] += prix
    
    # Trier par nombre de places réservées
    films_tries = sorted(reservations_par_film.items(), key=lambda x: x[1], reverse=True)
    
    if films_tries:
        for i, (film_id, nb_places) in enumerate(films_tries[:5], 1):
            film = storage.get_film(film_id)
            film_titre = film.titre if film else "Film inconnu"
            revenu = revenus_par_film[film_id]
            print(f"{i}. {film_titre}")
            print(f"   Places réservées: {nb_places} - Revenus: {revenu:.2f}€")
    else:
        print("Aucune donnée disponible")
    
    # Catégories les plus populaires
    print("\n🎭 CATÉGORIES LES PLUS POPULAIRES")
    print("-" * 50)
    
    categories = defaultdict(int)
    for film_id, nb_places in reservations_par_film.items():
        film = storage.get_film(film_id)
        if film:
            categories[film.categorie] += nb_places
    
    if categories:
        categories_triees = sorted(categories.items(), key=lambda x: x[1], reverse=True)
        for i, (cat, nb_places) in enumerate(categories_triees[:5], 1):
            print(f"{i}. {cat}: {nb_places} places")
    else:
        print("Aucune donnée disponible")
    
    # Horaires les plus demandés
    print("\n⏰ HORAIRES LES PLUS DEMANDÉS")
    print("-" * 50)
    
    horaires = defaultdict(int)
    for res in reservations:
        horaires[res.horaire] += len(res.places)
    
    if horaires:
        horaires_tries = sorted(horaires.items(), key=lambda x: x[1], reverse=True)
        for i, (horaire, nb_places) in enumerate(horaires_tries[:5], 1):
            print(f"{i}. {horaire}: {nb_places} places")
    else:
        print("Aucune donnée disponible")
    
    # Utilisateurs les plus actifs
    print("\n👥 UTILISATEURS LES PLUS ACTIFS")
    print("-" * 50)
    
    utilisateurs_tries = sorted(utilisateurs, key=lambda u: u.nombre_resa, reverse=True)
    
    if utilisateurs_tries:
        for i, user in enumerate(utilisateurs_tries[:5], 1):
            if user.nombre_resa > 0:
                print(f"{i}. {user.prenom} {user.nom}: {user.nombre_resa} réservation(s)")
    else:
        print("Aucun utilisateur actif")
    
    input("\n\nAppuyez sur Entrée...")


def room_map(representation_id: str, salle_id: str) -> List[List[str]]:
    """Retourne la carte 2D des sièges pour une représentation dans une salle"""
    salles_entry = storage.get_salle_seating(salle_id, representation_id)
    if salles_entry is None:
        print(f"Aucune carte trouvée pour la représentation {representation_id} dans la salle {salle_id}.")
        return []
    return getattr(salles_entry, 'seating_map', [])