from typing import List, Optional, Tuple
from datetime import datetime, date
from python.models import Film, Salle_info, Utilisateur, Reservation, Representation
from python.visuals import clear_screen
import storage
import getpass


def calculate_age(date_naissance: str) -> int:
    """Calculate age from birth date string (YYYY-MM-DD)"""
    try:
        birth_date = datetime.strptime(date_naissance, "%Y-%m-%d").date()
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except:
        return 0


def verify_age_restriction(user: Utilisateur, film: Film) -> bool:
    """Verify if user meets age requirement for film"""
    user_age = calculate_age(user.date_naissance)
    return user_age >= film.age_min


def calculate_ticket_price(salle: Salle_info, seat: str) -> float:
    """Calculate price based on seat type (VIP or normal)"""
    row_letter = seat[0]
    row_idx = ord(row_letter) - 65  # A=0, B=1, etc.
    
    if row_idx < salle.nombre_rangees_vip:
        return 15.0  # VIP price
    else:
        return 9.0  # Normal price


def list_films():
    """Display all available films"""
    clear_screen()
    print("=== FILMS DISPONIBLES ===\n")
    
    films = storage.list_films()
    if not films:
        print("Aucun film disponible.")
    else:
        for i, f in enumerate(films, 1):
            print(f"{i}. {f.titre}")
            print(f"   Durée: {f.duree}min | Catégorie: {f.categorie} | Âge minimum: {f.age_min}+")
            if f.horaires:
                print(f"   Horaires: {', '.join(f.horaires)}")
            print()
    
    input("Appuyez sur Entrée pour revenir au menu...")


def search_films():
    """Search films by title, category, or age restriction"""
    clear_screen()
    print("=== RECHERCHER UN FILM ===\n")
    print("1) Rechercher par titre")
    print("2) Rechercher par catégorie")
    print("3) Filtrer par âge minimum")
    print("0) Retour")
    
    choix = input("\nChoix: ").strip()
    
    films = storage.list_films()
    results = []
    
    if choix == "1":
        terme = input("\nEntrez le titre (ou partie du titre): ").strip().lower()
        results = [f for f in films if terme in f.titre.lower()]
    
    elif choix == "2":
        print("\nCatégories disponibles:")
        categories = set(f.categorie for f in films)
        for cat in sorted(categories):
            print(f"  - {cat}")
        
        categorie = input("\nEntrez la catégorie: ").strip()
        results = [f for f in films if f.categorie.lower() == categorie.lower()]
    
    elif choix == "3":
        try:
            age_max = int(input("\nAfficher les films pour quel âge maximum? "))
            results = [f for f in films if f.age_min <= age_max]
        except ValueError:
            print("Âge invalide.")
            input("Appuyez sur Entrée...")
            return
    
    elif choix == "0":
        return
    
    else:
        print("Choix invalide.")
        input("Appuyez sur Entrée...")
        return
    
    # Display results
    clear_screen()
    print("=== RÉSULTATS DE RECHERCHE ===\n")
    
    if not results:
        print("Aucun film trouvé.")
    else:
        for i, f in enumerate(results, 1):
            print(f"{i}. {f.titre}")
            print(f"   Durée: {f.duree}min | Catégorie: {f.categorie} | Âge minimum: {f.age_min}+")
            if f.horaires:
                print(f"   Horaires: {', '.join(f.horaires)}")
            print()
    
    input("Appuyez sur Entrée pour revenir au menu...")


def display_seating_map(seating_map: List[List[str]], salle: Salle_info) -> None:
    """Display the seating map with VIP section highlighted"""
    print("\n=== PLAN DE LA SALLE ===\n")
    print("Légende: [o] = Disponible | [x] = Occupé | [V] = VIP Disponible | [X] = VIP Occupé")
    print(f"\nÉcran")
    print("=" * (len(seating_map[0]) * 4 + 5))
    print()
    
    # Column numbers
    print("     ", end="")
    for col in range(len(seating_map[0])):
        print(f"{col+1:2}  ", end="")
    print("\n")
    
    # Rows with letters
    for row_idx, row in enumerate(seating_map):
        row_letter = chr(65 + row_idx)  # A, B, C, etc.
        is_vip = row_idx < salle.nombre_rangees_vip
        
        print(f"{row_letter}  ", end="")
        for seat in row:
            if is_vip:
                display = "[V]" if seat == 'o' else "[X]"
            else:
                display = f"[{seat}]"
            print(f" {display}", end="")
        
        if is_vip:
            print("  ← VIP", end="")
        print()
    
    print()


def select_seats(seating_map: List[List[str]], salle: Salle_info, num_seats: int) -> List[str]:
    """Allow user to select seats interactively"""
    selected_seats = []
    
    while len(selected_seats) < num_seats:
        display_seating_map(seating_map, salle)
        
        print(f"\nSièges sélectionnés: {', '.join(selected_seats) if selected_seats else 'Aucun'}")
        print(f"Sièges restants à sélectionner: {num_seats - len(selected_seats)}")
        
        seat_input = input("\nEntrez un siège (ex: A5) ou 'annuler' pour recommencer: ").strip().upper()
        
        if seat_input == "ANNULER":
            selected_seats = []
            continue
        
        # Validate format
        if len(seat_input) < 2 or not seat_input[0].isalpha() or not seat_input[1:].isdigit():
            print("❌ Format invalide. Utilisez le format: Lettre + Numéro (ex: A5)")
            input("Appuyez sur Entrée...")
            continue
        
        row_letter = seat_input[0]
        col_num = int(seat_input[1:])
        
        row_idx = ord(row_letter) - 65
        col_idx = col_num - 1
        
        # Validate bounds
        if row_idx < 0 or row_idx >= len(seating_map):
            print("❌ Rangée invalide.")
            input("Appuyez sur Entrée...")
            continue
        
        if col_idx < 0 or col_idx >= len(seating_map[0]):
            print("❌ Colonne invalide.")
            input("Appuyez sur Entrée...")
            continue
        
        # Check availability
        if seating_map[row_idx][col_idx] == 'x':
            print("❌ Ce siège est déjà occupé.")
            input("Appuyez sur Entrée...")
            continue
        
        if seat_input in selected_seats:
            print("❌ Vous avez déjà sélectionné ce siège.")
            input("Appuyez sur Entrée...")
            continue
        
        selected_seats.append(seat_input)
        print(f"✅ Siège {seat_input} ajouté.")
    
    return selected_seats


def buy_ticket(user: Utilisateur):
    """Complete ticket purchase flow with age verification and payment"""
    clear_screen()
    print("=== RÉSERVER UNE PLACE ===\n")
    
    # Step 1: Select film
    films = storage.list_films()
    if not films:
        print("Aucun film disponible.")
        input("Appuyez sur Entrée...")
        return
    
    print("Films disponibles:\n")
    for i, film in enumerate(films, 1):
        print(f"{i}. {film.titre} ({film.duree}min) [{film.categorie}] - Âge minimum: {film.age_min}+")
    
    try:
        choix_film = int(input("\nChoisissez un film (0 pour annuler): "))
        if choix_film == 0:
            return
        if choix_film < 1 or choix_film > len(films):
            print("Choix invalide.")
            input("Appuyez sur Entrée...")
            return
        
        film = films[choix_film - 1]
    except ValueError:
        print("Entrée invalide.")
        input("Appuyez sur Entrée...")
        return
    
    # Age verification
    if not verify_age_restriction(user, film):
        user_age = calculate_age(user.date_naissance)
        print(f"\n❌ Désolé, vous devez avoir au moins {film.age_min} ans pour voir ce film.")
        print(f"Votre âge: {user_age} ans")
        input("Appuyez sur Entrée...")
        return
    
    # Step 2: Select time slot
    clear_screen()
    print(f"=== {film.titre} ===\n")
    
    if not film.horaires:
        print("Aucun horaire disponible pour ce film.")
        input("Appuyez sur Entrée...")
        return
    
    print("Horaires disponibles:\n")
    for i, horaire in enumerate(film.horaires, 1):
        print(f"{i}. {horaire}")
    
    try:
        choix_horaire = int(input("\nChoisissez un horaire (0 pour annuler): "))
        if choix_horaire == 0:
            return
        if choix_horaire < 1 or choix_horaire > len(film.horaires):
            print("Choix invalide.")
            input("Appuyez sur Entrée...")
            return
        
        horaire = film.horaires[choix_horaire - 1]
    except ValueError:
        print("Entrée invalide.")
        input("Appuyez sur Entrée...")
        return
    
    # Find representation and assigned room
    representations = storage.list_representations()
    representation = None
    for rep in representations:
        if rep.film_id == film.id and rep.horaire == horaire:
            representation = rep
            break
    
    if not representation:
        print(f"\n❌ Aucune représentation trouvée pour {film.titre} à {horaire}.")
        input("Appuyez sur Entrée...")
        return
    
    # Find which room this representation is in
    salles = storage.list_salles()
    salle = None
    for s in salles:
        if representation.id in s.id_representations:
            salle = s
            break
    
    if not salle:
        print(f"\n❌ Aucune salle assignée pour cette représentation.")
        input("Appuyez sur Entrée...")
        return
    
    # Step 3: Get seating map
    salles_entry = storage.get_salle_seating(salle.id, representation.id)
    if not salles_entry or not salles_entry.seating_map:
        print("\n❌ Plan de salle non disponible.")
        input("Appuyez sur Entrée...")
        return
    
    seating_map = salles_entry.seating_map
    
    # Step 4: Select number of seats
    clear_screen()
    print(f"=== {film.titre} à {horaire} ===")
    print(f"Salle {salle.numero}\n")
    
    try:
        num_seats = int(input("Combien de places souhaitez-vous réserver? "))
        if num_seats < 1:
            print("Nombre invalide.")
            input("Appuyez sur Entrée...")
            return
    except ValueError:
        print("Entrée invalide.")
        input("Appuyez sur Entrée...")
        return
    
    # Step 5: Select seats
    selected_seats = select_seats(seating_map, salle, num_seats)
    
    if not selected_seats:
        print("Aucun siège sélectionné.")
        input("Appuyez sur Entrée...")
        return
    
    # Step 6: Calculate total price
    clear_screen()
    print("=== RÉCAPITULATIF DE LA RÉSERVATION ===\n")
    print(f"Film: {film.titre}")
    print(f"Horaire: {horaire}")
    print(f"Salle: {salle.numero}")
    print(f"\nSièges sélectionnés:")
    
    total_price = 0.0
    for seat in selected_seats:
        price = calculate_ticket_price(salle, seat)
        seat_type = "VIP" if price == 15.0 else "Normal"
        print(f"  - {seat} ({seat_type}): {price:.2f}€")
        total_price += price
    
    print(f"\nPrix total: {total_price:.2f}€")
    
    # Step 7: Confirmation
    confirmation = input("\nConfirmer la réservation? (oui/non): ").strip().lower()
    
    if confirmation != "oui":
        print("Réservation annulée.")
        input("Appuyez sur Entrée...")
        return
    
    # Step 8: Process payment (simulated)
    print("\n💳 Traitement du paiement...")
    print("✅ Paiement accepté!")
    
    # Step 9: Update seating map
    for seat in selected_seats:
        row_letter = seat[0]
        col_num = int(seat[1:])
        row_idx = ord(row_letter) - 65
        col_idx = col_num - 1
        seating_map[row_idx][col_idx] = 'x'
    
    storage.update_salle_seating(salle.id, representation.id, seating_map)
    
    # Step 10: Create reservation
    reservation = Reservation(
        utilisateur_id=user.id,
        salle_id=salle.id,
        film_id=film.id,
        representation_id=representation.id,
        horaire=horaire,
        places=selected_seats
    )
    storage.add_reservation(reservation)
    
    # Update user reservation count
    user.nombre_resa += 1
    storage.update_utilisateur(user)
    
    # Step 11: Confirmation message
    clear_screen()
    print("=" * 50)
    print("🎉 RÉSERVATION CONFIRMÉE 🎉")
    print("=" * 50)
    print(f"\nFilm: {film.titre}")
    print(f"Horaire: {horaire}")
    print(f"Salle: {salle.numero}")
    print(f"Places: {', '.join(selected_seats)}")
    print(f"Prix total: {total_price:.2f}€")
    print(f"\nNuméro de réservation: {reservation.id}")
    print("\n📧 Un email de confirmation a été envoyé à:", user.email)
    print("\nPrésentez ce numéro de réservation à l'entrée.")
    print("=" * 50)
    
    input("\nAppuyez sur Entrée pour revenir au menu...")


def view_my_reservations(user: Utilisateur):
    """Display user's reservations with option to cancel"""
    clear_screen()
    print("=== MES RÉSERVATIONS ===\n")
    
    reservations = storage.get_user_reservations(user.id)
    
    if not reservations:
        print("Vous n'avez aucune réservation.")
        input("\nAppuyez sur Entrée...")
        return
    
    print(f"Vous avez {len(reservations)} réservation(s):\n")
    
    for i, res in enumerate(reservations, 1):
        film = storage.get_film(res.film_id)
        film_titre = film.titre if film else "Film inconnu"
        
        salle = storage.get_salle(res.salle_id)
        salle_num = salle.numero if salle else "?"
        
        # Calculate price
        total_price = 0.0
        if salle:
            for seat in res.places:
                total_price += calculate_ticket_price(salle, seat)
        
        print(f"{i}. {film_titre}")
        print(f"   Horaire: {res.horaire}")
        print(f"   Salle: {salle_num}")
        print(f"   Places: {', '.join(res.places)}")
        print(f"   Prix: {total_price:.2f}€")
        print(f"   ID: {res.id}")
        print()
    
    # Option to cancel
    print("Options:")
    print("1) Annuler une réservation")
    print("0) Retour")
    
    choix = input("\nChoix: ").strip()
    
    if choix == "1":
        cancel_reservation(user, reservations)
    elif choix == "0":
        return
    else:
        print("Choix invalide.")
        input("Appuyez sur Entrée...")


def cancel_reservation(user: Utilisateur, reservations: List[Reservation]):
    """Cancel a reservation and free up seats"""
    print("\n=== ANNULER UNE RÉSERVATION ===\n")
    
    try:
        choix = int(input("Entrez le numéro de la réservation à annuler (0 pour retour): "))
        if choix == 0:
            return
        
        if choix < 1 or choix > len(reservations):
            print("Choix invalide.")
            input("Appuyez sur Entrée...")
            return
        
        reservation = reservations[choix - 1]
        
        # Confirmation
        film = storage.get_film(reservation.film_id)
        film_titre = film.titre if film else "Film inconnu"
        
        print(f"\nVous êtes sur le point d'annuler:")
        print(f"Film: {film_titre}")
        print(f"Horaire: {reservation.horaire}")
        print(f"Places: {', '.join(reservation.places)}")
        
        confirmation = input("\nConfirmer l'annulation? (oui/non): ").strip().lower()
        
        if confirmation != "oui":
            print("Annulation abandonnée.")
            input("Appuyez sur Entrée...")
            return
        
        # Free up seats in seating map
        representation = storage.get_representation(reservation.representation_id)
        
        if representation:
            salles_entry = storage.get_salle_seating(reservation.salle_id, representation.id)
            if salles_entry and salles_entry.seating_map:
                seating_map = salles_entry.seating_map
                
                for seat in reservation.places:
                    row_letter = seat[0]
                    col_num = int(seat[1:])
                    row_idx = ord(row_letter) - 65
                    col_idx = col_num - 1
                    
                    if 0 <= row_idx < len(seating_map) and 0 <= col_idx < len(seating_map[0]):
                        seating_map[row_idx][col_idx] = 'o'
                
                storage.update_salle_seating(reservation.salle_id, representation.id, seating_map)
        
        # Remove reservation from database
        db = storage.load_db()
        db['reservations'] = [r for r in db.get('reservations', []) if r.get('id') != reservation.id]
        storage.save_db(db)
        
        # Update user reservation count
        user.nombre_resa = max(0, user.nombre_resa - 1)
        storage.update_utilisateur(user)
        
        print("\n✅ Réservation annulée avec succès.")
        
    except ValueError:
        print("Entrée invalide.")
    
    input("\nAppuyez sur Entrée...")


def profile_personnel_info(user: Utilisateur):
    """Display and edit personal information"""
    clear_screen()
    print("=== INFORMATIONS PERSONNELLES ===\n")
    print(f"Nom: {user.nom}")
    print(f"Prénom: {user.prenom}")
    print(f"Date de naissance: {user.date_naissance}")
    print(f"Âge: {calculate_age(user.date_naissance)} ans")
    print(f"Email: {user.email}")
    print(f"Rôle: {user.role}")
    print(f"Nombre de réservations: {user.nombre_resa}")
    print("\n")
    print("1) Modifier mes informations")
    print("0) Retour")
    
    choix = input("\nChoix: ").strip()
    
    if choix == "1":
        modif_profile_personnel_info(user)
    elif choix == "0":
        return
    else:
        print("Choix invalide.")
        input("Appuyez sur Entrée...")


def modif_profile_personnel_info(user: Utilisateur):
    """Modify personal information"""
    clear_screen()
    print("=== MODIFIER MES INFORMATIONS ===\n")
    
    print("Laissez vide pour conserver la valeur actuelle.\n")
    
    new_nom = input(f"Nom ({user.nom}): ").strip() or user.nom
    new_prenom = input(f"Prénom ({user.prenom}): ").strip() or user.prenom
    new_email = input(f"Email ({user.email}): ").strip() or user.email
    
    # Optionally change password
    change_pwd = input("\nChanger le mot de passe? (oui/non): ").strip().lower()
    if change_pwd == "oui":
        new_password = getpass.getpass("Nouveau mot de passe: ")
        confirm_password = getpass.getpass("Confirmer le mot de passe: ")
        
        if new_password != confirm_password:
            print("\n❌ Les mots de passe ne correspondent pas.")
            input("Appuyez sur Entrée...")
            return
        
        if len(new_password) < 6:
            print("\n❌ Le mot de passe doit contenir au moins 6 caractères.")
            input("Appuyez sur Entrée...")
            return
        
        user.set_password(new_password)
        print("✅ Mot de passe mis à jour.")
    
    user.nom = new_nom
    user.prenom = new_prenom
    user.email = new_email
    
    storage.update_utilisateur(user)
    
    print("\n✅ Informations mises à jour avec succès.")
    input("Appuyez sur Entrée...")