from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple
import uuid
import os
import hashlib
import binascii
from datetime import datetime


def gen_id() -> str:
    """Génère un identifiant unique"""
    return str(uuid.uuid4())


# Constants
SALT_LENGTH = 16
ITERATIONS = 100_000
PASSWORD_ALGORITHM = 'sha256'


@dataclass
class Film:
    titre: str
    duree: int
    categorie: str
    age_min: int = 0
    horaires: List[str] = field(default_factory=list)
    id: str = field(default_factory=gen_id)

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> 'Film':
        return Film(
            titre=d.get('titre', ''),
            duree=d.get('duree', 0),
            categorie=d.get('categorie', ''),
            age_min=d.get('age_min', 0),
            horaires=d.get('horaires', []),
            id=d.get('id', gen_id()),
        )


@dataclass
class Salle_info:
    numero: int
    nombre_rangees_total: int
    nombre_rangees_vip: int
    nombre_colonnes: int
    id_representations: List[str] = field(default_factory=list)  # film id + horaire
    id: str = field(default_factory=gen_id)

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> 'Salle_info':
        return Salle_info(
            numero=d.get('numero', 0),
            nombre_rangees_total=d.get('nombre_rangees_total', 0),
            nombre_rangees_vip=d.get('nombre_rangees_vip', 0),
            nombre_colonnes=d.get('nombre_colonnes', 0),
            id_representations=d.get('id_representations', []),
            id=d.get('id', gen_id()),
        )


@dataclass
class Utilisateur:
    nom: str
    prenom: str
    date_naissance: str  # format ISO YYYY-MM-DD
    nombre_resa: int = 0
    role: str = 'client'  # 'client' ou 'admin'
    email: str = ''
    password_salt: str = ''  # hex
    password_hash: str = ''  # hex
    id: str = field(default_factory=gen_id)

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> 'Utilisateur':
        return Utilisateur(
            nom=d.get('nom', ''),
            prenom=d.get('prenom', ''),
            date_naissance=d.get('date_naissance', ''),
            nombre_resa=d.get('nombre_resa', 0),
            role=d.get('role', 'client'),
            email=d.get('email', ''),
            password_salt=d.get('password_salt', ''),
            password_hash=d.get('password_hash', ''),
            id=d.get('id', gen_id()),
        )

    def set_password(self, password: str) -> None:
        """Hash and set password using PBKDF2-HMAC-SHA256."""
        if not password or len(password) < 6:
            raise ValueError("Le mot de passe doit contenir au moins 6 caractères")
        salt = os.urandom(SALT_LENGTH)
        key = hashlib.pbkdf2_hmac(PASSWORD_ALGORITHM, password.encode('utf-8'), salt, ITERATIONS)
        self.password_salt = binascii.hexlify(salt).decode('ascii')
        self.password_hash = binascii.hexlify(key).decode('ascii')

    def verify_password(self, password: str) -> bool:
        """Vérifie si le mot de passe fourni correspond au hash stocké"""
        if not self.password_salt or not self.password_hash:
            return False
        try:
            salt = binascii.unhexlify(self.password_salt)
            key = hashlib.pbkdf2_hmac(PASSWORD_ALGORITHM, password.encode('utf-8'), salt, ITERATIONS)
            return binascii.hexlify(key).decode('ascii') == self.password_hash
        except Exception:
            return False
    
    def calculate_age(self) -> int:
        """Calcule l'âge de l'utilisateur à partir de sa date de naissance (format YYYY-MM-DD)"""
        try:
            birth_date = datetime.strptime(self.date_naissance, '%Y-%m-%d')
            today = datetime.now()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            return max(0, age)
        except (ValueError, TypeError):
            return 0
    
    def is_adult(self, age_min: int) -> bool:
        """Vérifie si l'utilisateur a l'âge minimum requis"""
        return self.calculate_age() >= age_min
    
    def get_full_name(self) -> str:
        """Retourne le nom complet de l'utilisateur"""
        return f"{self.prenom} {self.nom}"
    
    @property
    def is_admin(self) -> bool:
        """Vérifie si l'utilisateur est administrateur"""
        return self.role == 'admin'
    
@dataclass
class Representation:
    film_id: str
    horaire: str
    horaire_fin: str
    id: str = field(default_factory=gen_id)
    seating_map: List[List[str]] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> 'Representation':
        return Representation(
            film_id=d.get('film_id', ''),
            horaire=d.get('horaire', ''),
            horaire_fin=d.get('horaire_fin', ''),
            id=d.get('id', gen_id()),
            seating_map=d.get('seating_map', []),
        )

    def generate_map_from_salle(self, salle: 'Salle_info') -> None:
        """Crée une grille de places à partir de la configuration de la salle"""
        rows = max(0, int(salle.nombre_rangees_total))
        cols = max(0, int(salle.nombre_colonnes))
        self.seating_map = [['o' for _ in range(cols)] for _ in range(rows)]
    
    def get_available_seats_count(self) -> int:
        """Compte le nombre de places disponibles"""
        if not self.seating_map:
            return 0
        return sum(row.count('o') for row in self.seating_map)
    
    def get_seat_label(self, row: int, col: int) -> str:
        """Retourne le label d'une place (ex: A1, B5)"""
        if 0 <= row < 26:
            return f"{chr(65 + row)}{col + 1}"
        return f"R{row}C{col}"
    
@dataclass
class Reservation:
    utilisateur_id: str
    salle_id: str
    film_id: str
    horaire: str
    places: List[str] = field(default_factory=list)
    id: str = field(default_factory=gen_id)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> 'Reservation':
        return Reservation(
            utilisateur_id=d.get('utilisateur_id', ''),
            salle_id=d.get('salle_id', ''),
            film_id=d.get('film_id', ''),
            horaire=d.get('horaire', ''),
            places=d.get('places', []),
            id=d.get('id', gen_id()),
            created_at=d.get('created_at', datetime.now().isoformat()),
        )
    
    def get_total_price(self, vip_rows: List[int]) -> Tuple[int, int, int]:
        """
        Calcule le prix total de la réservation
        Returns: (prix_total, nombre_places_normales, nombre_places_vip)
        """
        normal_count = 0
        vip_count = 0
        
        for place in self.places:
            row_letter = place[0]
            row_idx = ord(row_letter) - 65
            if row_idx in vip_rows:
                vip_count += 1
            else:
                normal_count += 1
        
        total = (normal_count * 9) + (vip_count * 15)
        return total, normal_count, vip_count
    
    def get_places_count(self) -> int:
        """Retourne le nombre de places réservées"""
        return len(self.places)

@dataclass
class Salles:
    salle_id: str
    representation_id: List[str] = field(default_factory=list)
    # seating_map is stored as a 2D list (rows x cols) of 'O'/'X'
    seating_map: List[List[str]] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> 'Salles':
        return Salles(
            salle_id=d.get('salle_id', ''),
            representation_id=d.get('representation_id', []),
            seating_map=d.get('seating_map', {}),
        )