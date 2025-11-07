from PyQt6.QtWidgets import QMessageBox, QInputDialog, QListWidget, QDialog, QVBoxLayout, QPushButton
from datetime import datetime, timedelta
from python.models import Film, Salle_info, Representation
import storage


def gui_add_movie():
    titre, ok = QInputDialog.getText(None, "Ajouter un film", "Titre :")
    if not ok or not titre:
        return

    duree, ok = QInputDialog.getInt(None, "Ajouter un film", "Durée (minutes) :", 90, 1, 999)
    if not ok:
        return

    categorie, ok = QInputDialog.getText(None, "Ajouter un film", "Catégorie :")
    if not ok or not categorie:
        return

    age_min, ok = QInputDialog.getInt(None, "Ajouter un film", "Âge minimum :", 0, 0, 99)
    if not ok:
        return

    nbr, ok = QInputDialog.getInt(None, "Ajouter un film", "Nombre de représentations par jour :", 1, 1, 10)
    if not ok:
        return

    horaires = []
    for i in range(nbr):
        h, ok = QInputDialog.getText(None, "Horaires", f"Horaire {i+1} (HH:MM) :")
        if not ok or not h:
            return
        horaires.append(h)

    film = Film(titre=titre, duree=duree, categorie=categorie, age_min=age_min, horaires=horaires)
    storage.add_film(film)

    QMessageBox.information(None, "Succès", f"Film '{titre}' ajouté.")


def gui_add_room():
    numero, ok = QInputDialog.getInt(None, "Salle", "Numéro de la salle :", 1, 1, 999)
    if not ok:
        return

    total, ok = QInputDialog.getInt(None, "Salle", "Nombre total de rangées :", 5, 1, 50)
    if not ok:
        return

    vip, ok = QInputDialog.getInt(None, "Salle", "Nombre de rangées VIP :", 0, 0, total)
    if not ok:
        return

    colonnes, ok = QInputDialog.getInt(None, "Salle", "Nombre de colonnes :", 5, 1, 50)
    if not ok:
        return

    salle = Salle_info(numero=numero, nombre_rangees_total=total,
                       nombre_rangees_vip=vip, nombre_colonnes=colonnes)
    storage.add_salle(salle)
    QMessageBox.information(None, "Succès", f"Salle {numero} ajoutée.")


def gui_add_representation():
    films = storage.list_films()
    if not films:
        QMessageBox.warning(None, "Erreur", "Aucun film disponible.")
        return

    dialog = QDialog()
    dialog.setWindowTitle("Choisir un film")
    layout = QVBoxLayout(dialog)
    list_widget = QListWidget()
    for f in films:
        list_widget.addItem(f"{f.titre}")
    layout.addWidget(list_widget)

    btn_ok = QPushButton("Ok")
    layout.addWidget(btn_ok)
    btn_ok.clicked.connect(dialog.accept)

    if dialog.exec() != QDialog.DialogCode.Accepted or list_widget.currentRow() < 0:
        return

    film = films[list_widget.currentRow()]

    if not film.horaires:
        QMessageBox.warning(None, "Erreur", "Ce film n'a pas d'horaires.")
        return

    horaire, ok = QInputDialog.getItem(None, "Horaire", "Choisir un horaire :", film.horaires, 0, False)
    if not ok:
        return

    debut = datetime.strptime(horaire, "%H:%M")
    fin = debut + timedelta(minutes=film.duree)
    horaire_fin = fin.strftime("%H:%M")

    rep_id = f"{film.id}_{horaire}_{horaire_fin}"

    if storage.get_representation(rep_id):
        QMessageBox.warning(None, "Erreur", "Cette représentation existe déjà.")
        return

    rep = Representation(film_id=film.id, horaire=horaire, id=rep_id, horaire_fin=horaire_fin)
    storage.add_representation(rep)

    QMessageBox.information(None, "Succès", "Représentation ajoutée.")


def gui_assign_representation_to_room():
    reps = storage.list_representations()
    if not reps:
        QMessageBox.warning(None, "Erreur", "Aucune représentation.")
        return

    films = {r.id: storage.get_film(r.film_id).titre for r in reps}

    rep_labels = [f"{films[r.id]} ({r.horaire})" for r in reps]
    rep_label, ok = QInputDialog.getItem(None, "Représentation", "Choisir :", rep_labels, 0, False)
    if not ok:
        return

    rep = reps[rep_labels.index(rep_label)]

    salles = storage.list_salles()
    if not salles:
        QMessageBox.warning(None, "Erreur", "Aucune salle.")
        return

    salle_labels = [f"Salle {s.numero}" for s in salles]
    salle_label, ok = QInputDialog.getItem(None, "Salle", "Choisir :", salle_labels, 0, False)
    if not ok:
        return

    salle = salles[salle_labels.index(salle_label)]

    storage.assign_representation_to_room(rep.id, salle.id)
    QMessageBox.information(None, "Succès", "Représentation assignée.")
