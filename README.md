# Gestion de Cinéma - Système de Réservation

Un système complet de gestion de cinéma en Python permettant aux utilisateurs de consulter les films, effectuer des réservations et aux administrateurs de gérer les salles, films et représentations.

## Table des matières

- [Fonctionnalités](#fonctionnalités)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Structure du projet](#structure-du-projet)
- [Architecture](#architecture)
- [Base de données](#base-de-données)

## Fonctionnalités

### Pour les Utilisateurs
- **Consultation des films** : Voir la liste complète des films disponibles avec titre, durée, catégorie et restriction d'âge
- **Réservation de places** : Réserver des places directement depuis la liste des films
- **Gestion des réservations** : Visualiser l'historique des réservations
- **Profil personnel** : Consulter et modifier les informations personnelles (nom, prénom, email)
- **Contrôle d'accès** : Vérification automatique des restrictions d'âge pour chaque film

### Pour les Administrateurs
- **Gestion des films** : Ajouter de nouveaux films avec titre, durée, catégorie, restriction d'âge et horaires
- **Gestion des salles** : Créer des salles avec configuration (nombre de rangées, colonnes, VIP)
- **Gestion des représentations** : Ajouter des représentations de films avec horaires
- **Assignation des représentations** : Assigner les représentations à des salles
- **Validation des données** : Vérifications pour éviter les doublons et les données invalides

### Système de Réservation
- **Plan de salle interactif** : Visualisation claire des places disponibles et réservées
- **Sécurité des réservations** : Vérification des places disponibles avant confirmation
- **Suivi des réservations** : Compteur de réservations par utilisateur

## Installation

### Prérequis
- Python 3.8+

### Dépendances
Installez le paquet requis :
```
pip install art
```

## Utilisation

### Démarrage
Pour lancer l'application :
```
py main.py
```

### Flux utilisateur

#### 1. Authentification
- Saisissez votre email et mot de passe
- Ou créez un nouveau compte (nom, prénom, date de naissance, email, mot de passe)

#### 2. Menu Utilisateur
```
1) Voir les films disponibles
2) Réserver une salle
3) Voir mes réservations
4) Voir mes informations personnelles
0) Retour au menu principal
```

#### 3. Processus de Réservation
1. Consultez la liste des films
2. Sélectionnez un film pour voir les représentations disponibles
3. Choisissez une représentation (horaire)
4. Sélectionnez une salle
5. Visualisez le plan de la salle :
   - `o` = Place disponible
   - `x` = Place réservée
6. Entrez les places désirées (ex: A1,A2,B3)
7. Confirmez votre réservation

#### 4. Menu Admin
```
1) Ajouter un film
2) Ajouter une salle
3) Ajouter une représentation
4) Assigner une représentation à une salle
0) Retour au menu principal
```

## Structure du projet

```
projet-python-ING1-GIA2-PROCOPPE_BEAU/
├── main.py                 # Point d'entrée principal
├── storage.py              # Gestion de la base de données JSON
├── db.json                 # Fichier de données (auto-généré)
├── README.md               # Ce fichier
└── python/
    ├── models.py           # Définition des classes de données
    ├── admin_functions.py  # Fonctions administrateur
    ├── admin_gui.py        # Interface administrateur
    ├── user_functions.py   # Fonctions utilisateur et réservation
    ├── user_gui.py         # Interface utilisateur
    └── visuals.py          # Utilitaires d'affichage
```

## Architecture

### Modèles de données

#### Film
```python
- titre: str
- duree: int (minutes)
- categorie: str
- age_min: int
- horaires: List[str]
- id: str (UUID)
```

#### Utilisateur
```python
- nom: str
- prenom: str
- date_naissance: str (YYYY-MM-DD)
- email: str
- role: str ('client' ou 'admin')
- nombre_resa: int
- password_hash: str (PBKDF2-HMAC-SHA256)
- id: str (UUID)
```

#### Salle_info
```python
- numero: int
- nombre_rangees_total: int
- nombre_rangees_vip: int
- nombre_colonnes: int
- id_representations: List[str]
- id: str (UUID)
```

#### Representation
```python
- film_id: str
- horaire: str (HH:MM)
- horaire_fin: str (HH:MM)
- id: str (UUID)
```

#### Reservation
```python
- utilisateur_id: str
- salle_id: str
- film_id: str
- horaire: str
- places: List[str] (ex: ["A1", "A2"])
- id: str (UUID)
```

## Base de données

La base de données utilise JSON (`db.json`) avec la structure suivante :

```json
{
  "films": [],
  "salle_info": [],
  "utilisateurs": [],
  "representations": [],
  "reservations": [],
  "salles": []
}
```

### Fonctions principales de storage.py

| Fonction | Description |
|----------|-------------|
| `list_films()` | Récupère tous les films |
| `add_film(film)` | Ajoute un nouveau film |
| `list_salles()` | Récupère toutes les salles |
| `add_salle(salle)` | Ajoute une nouvelle salle |
| `list_representations()` | Récupère toutes les représentations |
| `add_representation(rep)` | Ajoute une représentation |
| `add_reservation(reservation)` | Ajoute une réservation |
| `assign_representation_to_room()` | Assigne une représentation à une salle |
| `authenticate_user(email, password)` | Authentifie un utilisateur |
| `authenticate_admin(email, password)` | Authentifie un administrateur |

## Sécurité

- **Hashage des mots de passe** : Utilise PBKDF2-HMAC-SHA256 avec salt
- **Validation des données** : Vérification des formats et des limites
- **Contrôle d'accès** : Distinction entre rôles admin et client
- **Vérification d'âge** : Restriction automatique des films selon l'âge minimum

## Exemple d'utilisation

### Ajouter un film (Admin)
1. Se connecter comme admin
2. Sélectionner "Ajouter un film"
3. Entrer les informations (titre, durée, catégorie, âge minimum, horaires)
4. Confirmer l'ajout

### Réserver une place (Utilisateur)
1. Se connecter comme utilisateur
2. Sélectionner "Voir les films disponibles"
3. Choisir un film pour voir les représentations
4. Sélectionner une représentation et une salle
5. Visualiser le plan et choisir les places
6. Confirmer la réservation

## Améliorations futures

- Système de paiement en ligne
- Annulation/modification de réservations
- Historique complet des utilisateurs
- Export de rapports
- Interface web avec Flask/Django
- Tests unitaires automatisés
- Système de notation des films

## Contributeurs

- [Sam Procoppe](https://github.com/Samito-05)
- [Alexis Beau](https://github.com/Beaualexis)
- [Elias Gaudare](https://github.com/Eliasgdr)

## Licence

Ce projet est fourni à titre éducatif.