import json
from pathlib import Path
from typing import Dict, Any, List, Optional

from python.models import Film, Salle_info, Utilisateur, Representation, Reservation, Salles


DB_PATH = Path(__file__).parent / 'db.json'


def _empty_db() -> Dict[str, List[Dict[str, Any]]]:
    return {
        "films": [],
        "salle_info": [],
        "utilisateurs": [],
        "representations": [],
        "reservations": [],
        "salles": []
    }


def load_db() -> Dict[str, List[Dict[str, Any]]]:
    if not DB_PATH.exists():
        save_db(_empty_db())
        return _empty_db()
    with DB_PATH.open('r', encoding='utf-8') as f:
        return json.load(f)


def save_db(db: Dict[str, List[Dict[str, Any]]]):
    with DB_PATH.open('w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2, separators=(',', ':'))


def list_films() -> List[Film]:
    db = load_db()
    return [Film.from_dict(d) for d in db.get('films', [])]


def add_film(film: Film) -> None:
    db = load_db()
    db.setdefault('films', [])
    db['films'].append(film.to_dict())
    save_db(db)

def get_film(film_id: str) -> Optional[Film]:
    db = load_db()
    for film_dict in db.get("films", []):
        if film_dict.get("id") == film_id:
            return Film.from_dict(film_dict)
    return None

def list_salles() -> List[Salle_info]:
    db = load_db()
    return [Salle_info.from_dict(d) for d in db.get('salle_info', [])]


def add_salle(salle: Salle_info) -> None:
    db = load_db()
    db.setdefault('salle_info', [])
    db['salle_info'].append(salle.to_dict())
    save_db(db)

def get_salle(salle_id: str) -> Optional[Salle_info]:
    """Get a specific salle by ID"""
    db = load_db()
    for salle_dict in db.get("salle_info", []):
        if salle_dict.get("id") == salle_id:
            return Salle_info.from_dict(salle_dict)
    return None


def list_representations() -> List[Representation]:
    db = load_db()
    return [Representation.from_dict(d) for d in db.get('representations', [])]

def get_representation(representation_id: str) -> Optional[Representation]:
    db = load_db()
    for rep_dict in db.get("representations", []):
        if rep_dict.get("id") == representation_id:
            return Representation.from_dict(rep_dict)
    return None


def add_representation(representation: Representation) -> None:
    db = load_db()
    db.setdefault('representations', [])
    db['representations'].append(representation.to_dict())
    save_db(db)

def assign_representation_to_room(representation_id: str, salle_id: str) -> None:
    db = load_db()
    salles = db.get('salle_info', [])
    for salle_dict in salles:
        if salle_dict.get('id') == salle_id:
            id_representations = salle_dict.get('id_representations', [])
            if representation_id not in id_representations:
                id_representations.append(representation_id)
                salle_dict['id_representations'] = id_representations
            break
    # Create a Salles entry for this representation assignment so seating map is stored
    # Find representation and salle_info objects
    from python.models import Salles, Salle_info

    rep = get_representation(representation_id)
    # build seating map only if representation and salle info found
    if rep is not None:
        # get salle info object
        salle_obj = None
        for s in db.get('salle_info', []):
            if s.get('id') == salle_id:
                salle_obj = Salle_info.from_dict(s)
                break
        if salle_obj is not None:
            # generate seating map on the representation instance
            try:
                rep.generate_map_from_salle(salle_obj)
            except Exception:
                # fallback: do nothing if generation fails
                pass
            # create a Salles entry specifically for this representation
            db.setdefault('salles', [])
            salles_entry = Salles(salle_id=salle_id, representation_id=[representation_id], seating_map=rep.seating_map)
            db['salles'].append(salles_entry.to_dict())

    save_db(db)


def add_salles_entry(salles_entry: Salles) -> None:
    db = load_db()
    db.setdefault('salles', [])
    db['salles'].append(salles_entry.to_dict())
    save_db(db)


def get_salle_seating(salle_id: str, representation_id: str) -> Optional[Salles]:
    db = load_db()
    for s in db.get('salles', []):
        # ensure structure matches: representation_id may be a list
        rep_ids = s.get('representation_id') or s.get('representation_id') or s.get('representation_id', [])
        # support different key naming if present
        if s.get('salle_id') == salle_id and representation_id in rep_ids:
            return Salles.from_dict(s)
    return None


def update_salle_seating(salle_id: str, representation_id: str, seating_map: List[List[str]]) -> None:
    """Update the seating map for a specific representation in a salle"""
    db = load_db()
    for s in db.get('salles', []):
        rep_ids = s.get('representation_id', [])
        if s.get('salle_id') == salle_id and representation_id in rep_ids:
            s['seating_map'] = seating_map
            save_db(db)
            return


def list_salles_entries() -> List[Salles]:
    db = load_db()
    return [Salles.from_dict(d) for d in db.get('salles', [])]

    
def list_utilisateurs() -> List[Utilisateur]:
    db = load_db()
    return [Utilisateur.from_dict(d) for d in db.get('utilisateurs', [])]


def add_utilisateur(user: Utilisateur) -> None:
    db = load_db()
    db.setdefault('utilisateurs', [])
    db['utilisateurs'].append(user.to_dict())
    save_db(db)


def find_user_by_email(email: str) -> Optional[Utilisateur]:
    for u in list_utilisateurs():
        if u.email.lower() == email.lower():
            return u
    return None


def create_user(nom: str, prenom: str, date_naissance: str, email: str, password: str, role: str = 'client') -> Utilisateur:
    existing = find_user_by_email(email)
    if existing is not None:
        raise ValueError('Utilisateur déjà existant pour cet email')
    u = Utilisateur(nom=nom, prenom=prenom, date_naissance=date_naissance, role=role, email=email)
    u.set_password(password)
    add_utilisateur(u)
    return u


def authenticate_user(email: str, password: str) -> Optional[Utilisateur]:
    u = find_user_by_email(email)
    if u is None:
        return None
    if u.verify_password(password):
        return u
    return None

def authenticate_admin(email: str, password: str) -> Optional[Utilisateur]:
    u = find_user_by_email(email)
    if u is None:
        return None
    if u.role != 'admin':
        return None
    if u.verify_password(password):
        return u
    return None

def update_utilisateur(user: Utilisateur) -> None:
    db = load_db()
    utilisateurs = db.get('utilisateurs', [])
    for i, user_dict in enumerate(utilisateurs):
        if user_dict.get('id') == user.id:
            utilisateurs[i] = user.to_dict()
            break
    save_db(db)

# Reservation functions
def add_reservation(reservation: Reservation) -> None:
    """Add a new reservation to the database"""
    db = load_db()
    db.setdefault('reservations', [])
    db['reservations'].append(reservation.to_dict())
    save_db(db)

def list_reservations() -> List[Reservation]:
    """List all reservations"""
    db = load_db()
    return [Reservation.from_dict(d) for d in db.get('reservations', [])]

def get_user_reservations(user_id: str) -> List[Reservation]:
    """Get all reservations for a specific user"""
    db = load_db()
    reservations = []
    for res_dict in db.get('reservations', []):
        if res_dict.get('utilisateur_id') == user_id:
            reservations.append(Reservation.from_dict(res_dict))
    return reservations