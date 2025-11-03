from dataclasses import dataclass, field, asdict
from typing import List, Optional
import uuid
import os
import hashlib
import binascii


def gen_id() -> str:
    return str(uuid.uuid4())


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
class Salle:
    numero: int
    nombre_rangees_total: int
    nombre_rangees_vip: int
    nombre_colonnes: int
    id_representations: List[str] = field(default_factory=list)  # film id + horaire
    id: str = field(default_factory=gen_id)

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> 'Salle':
        return Salle(
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
        salt = os.urandom(16)
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100_000)
        self.password_salt = binascii.hexlify(salt).decode('ascii')
        self.password_hash = binascii.hexlify(key).decode('ascii')

    def verify_password(self, password: str) -> bool:
        if not self.password_salt or not self.password_hash:
            return False
        salt = binascii.unhexlify(self.password_salt)
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100_000)
        return binascii.hexlify(key).decode('ascii') == self.password_hash
    
@dataclass
class Representation:
    film_id: str
    horaire: str
    id: str = field(default_factory=gen_id)

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> 'Representation':
        return Representation(
            film_id=d.get('film_id', ''),
            horaire=d.get('horaire', ''),
            id=d.get('id', gen_id()),
        )
    
@dataclass
class Reservation:
    utilisateur_id: str
    salle_id: str
    film_id: str
    horaire: str  # format ISO YYYY-MM-DDTHH:MM
    places: List[str] = field(default_factory=list)  # ex: ["A1", "A2"]
    id: str = field(default_factory=gen_id)

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
        )
