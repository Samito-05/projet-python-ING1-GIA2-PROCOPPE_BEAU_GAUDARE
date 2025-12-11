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
- **Recherche avancée** : Rechercher par titre, catégorie ou restriction d'âge
- **Réservation de places** : Réserver des places avec système VIP
  - Places normales : 9€
  - Places VIP : 15€
  - Visualisation en temps réel du prix total
- **Gestion des réservations** : Visualiser, annuler et modifier l'historique des réservations
- **Profil personnel** : Consulter et modifier les informations personnelles
- **Contrôle d'accès** : Vérification automatique des restrictions d'âge pour chaque film
- **Plan de salle interactif** (mode GUI) :
  - Sièges disponibles en cyan (#00d4ff)
  - Sièges VIP en violet (#d946ef)
  - Sièges réservés en rouge (#ff3333)
  - Sièges sélectionnés en jaune doré (#ffed4e)

### Pour les Administrateurs
- **Gestion des films** : Ajouter films avec titre, durée, catégorie, restriction d'âge et horaires
- **Gestion des salles** : Créer des salles avec configuration (rangées, colonnes, VIP)
- **Gestion des représentations** : Ajouter des représentations avec horaires
- **Assignation des représentations** : Assigner les représentations à des salles
- **Validation des données** : Vérifications pour éviter les doublons et données invalides

### Interface Utilisateur
- **Deux modes** : Terminal (CLI) et Interface Graphique (GUI)
- **Design moderne** : Thème sombre avec interface Tkinter (mode GUI)
- **Navigation fluide** : Menus clairs avec retour facile aux étapes précédentes
- **Responsive** : Fenêtres scrollables pour les listes longues

## Installation

### Prérequis
- Python 3.8+

### Dépendances
Installez le paquet requis :
```bash
pip install art
```

## Utilisation

### Deux modes disponibles

#### Mode Terminal (CLI)
```bash
python main.py
```
Permet une navigation textuelle simple avec menus en ligne de commande. Idéal pour tester rapidement ou utiliser en environnement sans GUI.

#### Mode Interface Graphique (GUI)
```bash
python gui_app.py
```
Propose une interface moderne avec Tkinter incluant un plan de salle interactif et affichage du prix en temps réel.

---

## Navigation en Terminal (main.py)

### Menu Principal
Au lancement de l'application :
```
1) Afficher les films
2) Se connecter
3) Créer un compte utilisateur
4) Accéder au panneau d'administration
0) Quitter
```

**Comment naviguer :**
- Entrez le numéro de votre choix et appuyez sur **Entrée**
- Le numéro `0` permet de retourner au menu précédent ou de quitter
- Après chaque action, un message "Appuyez sur Entrée pour revenir au menu..." s'affiche

### 1. Afficher les Films
Affiche la liste complète des films avec titre, durée, catégorie, âge minimum et horaires.

### 2. Se Connecter
```
Email: votre.email@example.com
Mot de passe: (caché)
```
Entrez vos identifiants pour accéder au menu utilisateur.

### 3. Créer un Compte Utilisateur
```
Nom: Dupont
Prénom: Jean
Date de naissance (YYYY-MM-DD): 1990-05-15
Email: jean.dupont@example.com
Mot de passe: (caché)
```
Un compte est créé et vous êtes connecté automatiquement.

### Menu Utilisateur
```
1) Voir les films disponibles
2) Rechercher un film
3) Réserver une place
4) Voir mes réservations
5) Voir mes informations personnelles
0) Retour au menu principal
```

#### 1) Voir les films disponibles
Affiche la liste complète des films avec leurs détails et horaires.

#### 2) Rechercher un film
```
1) Rechercher par titre
2) Rechercher par catégorie
3) Filtrer par âge minimum
0) Retour
```
- **Par titre** : Tapez le titre (ou partie du titre) pour obtenir des résultats partiels
- **Par catégorie** : Choisissez parmi les catégories disponibles
- **Par âge** : Entrez un âge maximum pour voir les films accessibles

#### 3) Réserver une place
Processus complet avec étapes :

1. **Sélectionner un film** : Entrez le numéro du film (0 pour annuler)
2. **Vérification d'âge** : Le système vérifie automatiquement
3. **Choisir un horaire** : Sélectionnez l'horaire parmi les représentations
4. **Nombre de places** : Entrez le nombre de sièges à réserver
5. **Sélectionner les sièges** :
   ```
   === PLAN DE LA SALLE ===
   Légende: [o] = Disponible | [x] = Occupé | [V] = VIP Disponible | [X] = VIP Occupé
   
        1  2  3  4  5  6
   A   [V] [V] [V] [o] [V] [o]  ← VIP (15€)
   B   [o] [x] [o] [x] [o] [x]  ← Normal (9€)
   ```
   - Entrez chaque siège au format `LETTRE + NUMÉRO` (ex: `A5`)
   - Tapez `ANNULER` pour recommencer
   - Les prix s'affichent pour chaque siège

6. **Récapitulatif** : Vérifiez vos choix et prix
7. **Confirmation** : Tapez `oui` pour confirmer
8. **Paiement simulé** : Le système confirme le paiement
9. **Confirmation finale** : Affichage du numéro de réservation

#### 4) Voir mes réservations
Affiche la liste de vos réservations avec options :
```
1) Annuler une réservation
0) Retour
```

Pour annuler, entrez le numéro de la réservation et confirmez avec `oui`. Les places sont libérées automatiquement.

#### 5) Voir mes informations personnelles
```
1) Modifier mes informations
0) Retour
```

**Modifier les informations :**
- Nom, prénom, email (les champs vides gardent la valeur actuelle)
- Changement de mot de passe optionnel (minimum 6 caractères)

### Menu Administrateur
Accessible via l'option `4` du menu principal :
```
1) Ajouter un film
2) Ajouter une salle
3) Ajouter une représentation
4) Assigner une représentation à une salle
0) Retour au menu principal
```

**1) Ajouter un film :**
```
Titre: Avatar 2
Durée (minutes): 192
Catégorie: Science-Fiction
Âge minimum: 12
Horaires (séparés par des virgules): 14:00, 17:30, 20:45
```

**2) Ajouter une salle :**
```
Numéro de salle: 1
Nombre de rangées total: 10
Nombre de rangées VIP: 3
Nombre de colonnes: 8
```

**3) Ajouter une représentation :**
```
Choisissez un film: [liste affichée]
Horaire (HH:MM): 20:45
Horaire de fin (HH:MM): 22:47
```

**4) Assigner une représentation à une salle :**
```
Choisissez une salle: [liste affichée]
Choisissez une représentation: [liste affichée]
```

---

## Navigation en Mode GUI (gui_app.py)

### Écran d'Authentification
- Connexion avec email et mot de passe
- Création de nouveau compte
- Interface stylisée avec thème sombre

### Dashboard Utilisateur
Menus visuels avec boutons pour :
- Voir les films disponibles
- Rechercher un film
- Réserver une place
- Consulter les réservations
- Gérer le profil

### Plan de Salle Interactif
Visualisation claire des places avec codes couleur :
- **Cyan** = Place normale disponible (9€)
- **Violet** = Place VIP disponible (15€)
- **Rouge** = Place réservée
- **Jaune** = Votre sélection

**Interaction :** Cliquez sur les places pour les sélectionner/désélectionner. Le prix total s'affiche en temps réel.

### Réservations Scrollables
Historique complet avec barre de défilement verticale. Affichage du film, horaire, salle, places et prix pour chaque réservation.

### Profil Personnel
Vue et édition en une seule fenêtre. Modification du nom, prénom, email et changement de mot de passe.

---

## Structure du projet

```
projet-python-ING1-GIA2-PROCOPPE_BEAU/
├── main.py                 # Point d'entrée terminal (CLI)
├── gui_app.py              # Point d'entrée interface graphique
├── storage.py              # Gestion de la base de données JSON
├── db.json                 # Fichier de données (auto-généré)
├── README.md               # Ce fichier
└── python/
    ├── models.py           # Définition des classes de données
    ├── admin_functions.py  # Fonctions administrateur
    ├── admin_gui.py        # Interface administrateur (GUI)
    ├── user_functions.py   # Fonctions utilisateur et réservation
    ├── user_gui.py         # Interface utilisateur (GUI)
    └── visuals.py          # Utilitaires d'affichage
```

## Architecture

### Modèles de données

**Film**
```python
- titre: str
- duree: int (minutes)
- categorie: str
- age_min: int
- horaires: List[str]
- id: str (UUID)
```

**Utilisateur**
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

**Salle_info**
```python
- numero: int
- nombre_rangees_total: int
- nombre_rangees_vip: int
- nombre_colonnes: int
- id_representations: List[str]
- id: str (UUID)
```

**Representation**
```python
- film_id: str
- horaire: str (HH:MM)
- horaire_fin: str (HH:MM)
- id: str (UUID)
```

**Reservation**
```python
- utilisateur_id: str
- salle_id: str
- film_id: str
- representation_id: str
- horaire: str
- places: List[str]
- id: str (UUID)
```

## Base de données

La base de données utilise JSON (`db.json`) avec la structure :

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
| `get_user_reservations(user_id)` | Récupère les réservations d'un utilisateur |
| `get_salle_seating(salle_id, rep_id)` | Récupère le plan de salle |
| `update_salle_seating(salle_id, rep_id, map)` | Met à jour le plan de salle |
| `authenticate_user(email, password)` | Authentifie un utilisateur |
| `authenticate_admin(email, password)` | Authentifie un administrateur |

## Sécurité

- **Hashage des mots de passe** : Utilise PBKDF2-HMAC-SHA256 avec salt
- **Validation des données** : Vérification des formats (email, date, etc.)
- **Contrôle d'accès** : Distinction entre rôles admin et client
- **Vérification d'âge** : Restriction automatique selon l'âge minimum
- **Protection des réservations** : Vérification de la disponibilité avant confirmation

## Système de Tarification

**Prix des places :**
- Place normale : 9€ (rangées standards)
- Place VIP : 15€ (premières rangées configurables)

**Exemple de calcul :**
```
3 places normales (A1, A2, A3) = 3 × 9€ = 27€
2 places VIP (B1, B2) = 2 × 15€ = 30€
Total = 57€
```

Le prix total est affiché en temps réel lors de la sélection des places.

---

## Contributeurs

- [Sam Procoppe](https://github.com/Samito-05)
- [Alexis Beau](https://github.com/Beaualexis)
- [Elias Gaudare](https://github.com/Eliasgdr)

## Licence

Ce projet est fourni à titre éducatif.
















































































































































































































































































































































































































































































































































































































































