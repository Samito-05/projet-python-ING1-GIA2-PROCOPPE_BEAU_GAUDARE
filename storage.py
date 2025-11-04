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
        json.dump(db, f, ensure_ascii=False, indent=2)


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
    save_db(db)

    
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
