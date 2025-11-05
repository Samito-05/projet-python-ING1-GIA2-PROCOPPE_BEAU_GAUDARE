from PyQt6.QtWidgets import QMessageBox, QInputDialog
import storage

def list_films():
    films = storage.list_films()
    if not films:
        QMessageBox.information(None, "Films", "Aucun film.")
        return

    msg = ""
    for f in films:
        msg += f"- {f.titre} ({f.duree} min) [{f.categorie}] Age min={f.age_min}\n"

    QMessageBox.information(None, "Films Disponibles", msg)


def buy_ticket():
    QMessageBox.information(None, "Réservation", "Fonctionnalité de réservation de salle à implémenter.")
